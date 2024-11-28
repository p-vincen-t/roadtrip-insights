import psycopg2
from psycopg2 import sql
import json
import os
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# Load environment variables from .env file
load_dotenv()

class DBManager:
    def __init__(self):
        self.db_name = os.getenv("POSTGRES_DB")
        self.db_user = os.getenv("POSTGRES_USER")
        self.db_password = os.getenv("POSTGRES_PASSWORD")
        self.db_host = os.getenv("POSTGRES_HOST")
        self.db_port = os.getenv("POSTGRES_PORT")
        self.influx_url = os.getenv("INFLUXDB_URL")
        self.influx_token = os.getenv("INFLUXDB_TOKEN")
        self.influx_org = os.getenv("INFLUXDB_ORG")
        self.influx_bucket = os.getenv("INFLUXDB_BUCKET")
        self.create_tables()

    def create_conn(self):
        conn = psycopg2.connect(
            dbname=self.db_name,
            user=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port
        )
        return conn

    def create_tables(self):
        commands = (
            """
            CREATE TABLE IF NOT EXISTS vehicles (
                id SERIAL PRIMARY KEY,
                plate_number VARCHAR(255) NOT NULL,
                model VARCHAR(255) NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS daily_data (
                id SERIAL PRIMARY KEY,
                date DATE NOT NULL,
                vehicle VARCHAR(255) NOT NULL,
                category VARCHAR(255) NOT NULL,
                amount REAL NOT NULL
            )
            """
        )
        conn = self.create_conn()
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        conn.commit()
        cur.close()
        conn.close()

    def insert_daily_data(self, date, vehicle, category, amount):
        sql = """INSERT INTO daily_data (date, vehicle, category, amount)
                 VALUES (%s, %s, %s, %s)"""
        conn = self.create_conn()
        cur = conn.cursor()
        cur.execute(sql, (date, vehicle, category, amount))
        conn.commit()
        cur.close()
        conn.close()

    def get_daily_data(self):
        conn = self.create_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM daily_data")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    def get_daily_trip_data(self):
        client = InfluxDBClient(url=self.influx_url, token=self.influx_token, org=self.influx_org)
        query_api = client.query_api()
        query = f'from(bucket:"{self.influx_bucket}") |> range(start: -1d)'
        tables = query_api.query(query)
        client.close()
        return tables

    def add_vehicle(self, plate, model):
        sql = """INSERT INTO vehicles (plate_number, model)
                 VALUES (%s, %s)"""
        conn = self.create_conn()
        cur = conn.cursor()
        cur.execute(sql, (plate, model))
        conn.commit()
        cur.close()
        conn.close()

    def list_vehicles(self):
        conn = self.create_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM vehicles")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    def write_influx_data(self, data):
        client = InfluxDBClient(url=self.influx_url, token=self.influx_token, org=self.influx_org)
        write_api = client.write_api(write_options=SYNCHRONOUS)
        point = Point("trip_data")
        for key, value in data.items():
            point = point.field(key, value)
        write_api.write(bucket=self.influx_bucket, org=self.influx_org, record=point)
        client.close()

    def clear_influxdb_data(self, start_date, end_date):
        client = InfluxDBClient(url=self.influx_url, token=self.influx_token, org=self.influx_org)
        delete_api = client.delete_api()
        start = f"{start_date}T00:00:00Z"
        stop = f"{end_date}T00:00:00Z"
        delete_api.delete(start, stop, '_measurement="trip_data"', bucket=self.influx_bucket, org=self.influx_org)
        client.close()

    def clear_sqlite_data(self):
        conn = self.create_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM daily_data")
        conn.commit()
        cur.close()
        conn.close()

    def close_influx_connection(self):
        pass
