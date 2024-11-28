import sqlite3
from influxdb_client import InfluxDBClient, Point
import os
from dotenv import load_dotenv
import pandas as pd
import logging

load_dotenv()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s') #Increased logging level

class DBManager:
    def __init__(self):
        self.sqlite_db = os.getenv("SQLITE_DB")
        self.influx_url = os.getenv("INFLUX_URL")
        self.influx_token = os.getenv("INFLUX_TOKEN")
        self.influx_org = os.getenv("INFLUX_ORG")
        self.influx_bucket = os.getenv("INFLUX_BUCKET")

        if not all([self.sqlite_db, self.influx_url, self.influx_token, self.influx_org, self.influx_bucket]):
            raise ValueError("Missing credentials in .env file.")

        try:
            self.influx_client = InfluxDBClient(url=self.influx_url, token=self.influx_token, org=self.influx_org)
            logging.info("Successfully connected to InfluxDB.")
        except Exception as e:
            logging.error(f"Error connecting to InfluxDB: {e}")
            raise

        self.create_sqlite_db()

    def create_sqlite_db(self):
        conn = sqlite3.connect(self.sqlite_db)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def insert_daily_data(self, date, category, amount):
        conn = sqlite3.connect(self.sqlite_db)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO daily_data (date, category, amount) VALUES (?, ?, ?)", (date, category, amount))
        conn.commit()
        conn.close()

    def get_daily_data(self):
        conn = sqlite3.connect(self.sqlite_db)
        cursor = conn.cursor()
        cursor.execute("SELECT date, category, amount FROM daily_data")
        data = cursor.fetchall()
        conn.close()
        return data

    def write_influx_data(self, data):
        write_api = self.influx_client.write_api()
        for record in data:
            cleaned_record = {k: v.replace('/', '') if isinstance(v, str) else v for k, v in record.items()}
            point = Point("trip").tag("vehicle", "BM125").fields(cleaned_record)
            write_api.write(bucket=self.influx_bucket, record=point)

    def clear_influxdb_data(self):
        query_api = self.influx_client.query_api()
        query = f'DELETE FROM "{self.influx_bucket}"'
        try:
            result = query_api.query_data_frame(query=query)
            return result
        except Exception as e:
            logging.error(f"Error clearing InfluxDB data: {e}")
            return None

    def close_influx_connection(self):
        self.influx_client.close()

    def get_daily_trip_data(self):
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
