# RoadTrip Insights - Vehicle Operational Data Management Application

This Streamlit application manages and analyzes vehicle operational data, including daily income/expenses and trip details. The purpose of the application is to provide a comprehensive dashboard for tracking and visualizing financial and trip data, helping users make informed decisions based on real-time data.

## Features

- **Daily Income & Expense Management:** Input and track daily income and expenses categorized by type (Revenue, Fuel, Repair, Spare Parts). Data is stored in a PostgreSQL database. ![Daily Expenses](images/financials.png)
- **Trip Data Handling:** Upload trip data from CSV or PDF files. Data is stored in an InfluxDB time-series database. ![Trip Timeline](images/upload.png)
- **Dashboard & Visualization:** Interactive charts and tables visualize financial data and trip reports (daily income/expenses, profit/loss, total distance, average trip duration, trip timeline).
- **Data Clearing:** Clear all trip data from InfluxDB.
- **Financial Chart Creation:** Create financial charts using provided data.
- **Trip Timeline Visualization:** Create timeline visualizations for trip data.
- **Trip Summary Table:** Create summary tables for trip data.
- **Daily Trip Mileage Chart:** Create charts showing daily trip count vs. mileage.
- **Expense vs. Revenue Chart:** Create charts showing expense vs. revenue over different timestamps.
- **Trip Efficiency Chart:** Create charts showing trip efficiency metrics.
- **Expense Forecasting Chart:** Create charts showing expense forecasting.

## Setup

1. **Prerequisites:**
   - Docker
   - Docker Compose
   - Python 3.9+
   - `pip install -r requirements.txt` (or `conda install --file requirements.txt`)

2. **Environment Variables:** Create a `.env` file with the following variables:
   - `POSTGRES_DB`: PostgreSQL database name (e.g., `bm125`)
   - `POSTGRES_USER`: PostgreSQL username (e.g., `bm125`)
   - `POSTGRES_PASSWORD`: PostgreSQL password (e.g., `bm125`)
   - `POSTGRES_HOST`: PostgreSQL host (e.g., `host.docker.internal`)
   - `POSTGRES_PORT`: PostgreSQL port (e.g., `5432`)
   - `INFLUXDB_URL`: InfluxDB URL (e.g., `http://localhost:8086`)
   - `INFLUXDB_TOKEN`: Your InfluxDB token
   - `INFLUXDB_ORG`: Your InfluxDB organization
   - `INFLUXDB_BUCKET`: Your InfluxDB bucket name (e.g., `bm125`)

3. **Run:**
   - `docker compose up -d`
   - Access the application at `http://localhost:8501`

## Usage

- Enter daily income and expenses using the provided form.
- Upload trip data using either a CSV or PDF file. CSV files should follow the specified header format.
- Use the interactive charts and tables to analyze financial and trip data.
- Use the "Clear Trip Data" button to clear all trip data from InfluxDB.

## Notes

- The PDF parsing functionality might require further refinement depending on the PDF's structure. CSV upload is generally more reliable.
- Ensure that InfluxDB is running and accessible before starting the application.

## Recent Changes

- Added debug statements to `db_manager.py` to print connection parameters and SQL commands being executed.
- Updated `visualization.py` to ensure the `data` parameter is always a DataFrame in the `create_daily_trip_mileage_chart` function.
