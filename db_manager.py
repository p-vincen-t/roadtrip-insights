import sqlite3
from influxdb_client import InfluxDBClient, Point, DeleteApi
import os
from dotenv import load_dotenv
import pandas as pd
import logging

# Load environment variables from .env file
load_dotenv()
# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class DBManager:
    def __init__(self):
        # Get database connection details from environment variables
        self.sqlite_db = os.getenv("SQLITE_DB")
        self.influx_url = os.getenv("INFLUX_URL")
        self.influx_token = os.getenv("INFLUX_TOKEN")
        self.influx_org = os.getenv("INFLUX_ORG")
        self.influx_bucket = os.getenv("INFLUX_BUCKET")

        # Check if all required environment variables are set
        if not all([self.sqlite_db, self.influx_url, self.influx_token, self.influx_org, self.influx_bucket]):
            raise ValueError("Missing credentials in .env file.")

        # Establish InfluxDB connection
        try:
            self.influx_client = InfluxDBClient(url=self.influx_url, token=self.influx_token, org=self.influx_org)
            logging.info("Successfully connected to InfluxDB.")
        except Exception as e:
            logging.error(f"Error connecting to InfluxDB: {e}")
            raise

        # Create SQLite database
        self.create_sqlite_db()

    def create_sqlite_db(self):
        # Create SQLite database and tables if they don't exist
        conn = sqlite3.connect(self.sqlite_db)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                vehicle TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vehicles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plate TEXT NOT NULL UNIQUE,
                model TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def insert_daily_data(self, date, vehicle, category, amount):
        # Insert daily financial data into SQLite database
        conn = sqlite3.connect(self.sqlite_db)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO daily_data (date, vehicle, category, amount) VALUES (?, ?, ?, ?)", (date, vehicle, category, amount))
        conn.commit()
        conn.close()

    def get_daily_data(self):
        # Retrieve daily financial data from SQLite database
        conn = sqlite3.connect(self.sqlite_db)
        cursor = conn.cursor()
        cursor.execute("SELECT date, vehicle, category, amount FROM daily_data")
        data = cursor.fetchall()
        conn.close()
        return data

    def get_vehicles(self):
        # Retrieve unique vehicle names from the database
        conn = sqlite3.connect(self.sqlite_db)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT vehicle FROM daily_data")
        vehicles = cursor.fetchall()
        conn.close()
        return [vehicle[0] for vehicle in vehicles]

    def add_vehicle(self, plate, model):
        # Add a new vehicle to the database
        conn = sqlite3.connect(self.sqlite_db)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO vehicles (plate, model) VALUES (?, ?)", (plate, model))
        conn.commit()
        conn.close()

    def list_vehicles(self):
        # List all vehicles in the database
        conn = sqlite3.connect(self.sqlite_db)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vehicles")
        vehicles = cursor.fetchall()
        conn.close()
        return vehicles

    def write_influx_data(self, data):
        # Write trip data to InfluxDB
        write_api = self.influx_client.write_api()
        for record in data:
            # Remove escape characters from data before writing to InfluxDB
            cleaned_record = {k: v.replace('/', '') if isinstance(v, str) else v for k, v in record.items()}
            point = Point("trip").tag("vehicle", cleaned_record["Vehicle Plate Number"]).field(cleaned_record)
            write_api.write(bucket=self.influx_bucket, record=point)

    def clear_influxdb_data(self, start_date, end_date):
        # Clear all data from the specified InfluxDB bucket
        delete_api = self.influx_client.delete_api()
        start = start_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        stop = end_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        try:
            delete_api.delete(start=start, stop=stop, predicate="_measurement=trip", bucket=self.influx_bucket, org=self.influx_org)
            return True
        except Exception as e:
            logging.error(f"Error clearing InfluxDB data: {e}")
            return False

    def clear_sqlite_data(self):
        # Clear all data from the SQLite database
        conn = sqlite3.connect(self.sqlite_db)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM daily_data")
        cursor.execute("DELETE FROM vehicles")
        conn.commit()
        conn.close()

    def close_influx_connection(self):
        # Close the InfluxDB connection
        self.influx_client.close()

    def get_daily_trip_data(self):
        # Retrieve daily trip data from InfluxDB
        query_api = self.influx_client.query_api()
        query = f'''
            from(bucket:"{self.influx_bucket}")
              |> range(start: -30d)
              |> filter(fn: (r) => r._measurement == "trip")
              |> group(columns: ["_time"])
              |> aggregateWindow(every: 1d, fn: count, createEmpty: false)
              |> rename(columns:{{_value: "Trip Count"}})
              |> join(
                other: from(bucket:"{self.influx_bucket}")
                  |> range(start: -30d)
                  |> filter(fn: (r) => r._measurement == "trip")
                  |> group(columns: ["_time"])
                  |> aggregateWindow(every: 1d, fn: sum, column: "Mileage (km)", createEmpty: false)
                  |> rename(columns:{{_value: "Mileage (km)"}})
              )
              |> keep(columns: ["_time", "Trip Count", "Mileage (km)"])
        '''
        try:
            logging.info(f"Executing InfluxDB query: {query}")
            result = query_api.query_data_frame(query=query)
            logging.info(f"InfluxDB query successful. Result: {result}")
            return result
        except Exception as e:
            logging.error(f"Error querying InfluxDB: {e}")
            return None
