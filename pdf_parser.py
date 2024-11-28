import camelot
import pandas as pd
from typing import List, Dict
import datetime
import logging
import re

# Configure logging to output to console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_trip_data(file_path: str, file_type: str) -> List[Dict]:
    try:
        if file_type == "pdf":
            tables = camelot.read_pdf(file_path, pages='all', flavor='stream')
            all_data = []
            for i, table in enumerate(tables):
                logging.info(f"Processing table {i+1} from PDF...")
                df = table.df
                if len(df) > 1:
                    #Rename columns to match expected format
                    df = df.rename(columns={
                        df.columns[0]: 'Vehicle Plate Number',
                        df.columns[1]: 'Trip State',
                        df.columns[2]: 'Start Time',
                        df.columns[3]: 'End Time',
                        df.columns[4]: 'Mileage (km)',
                        df.columns[5]: 'Duration',
                        df.columns[6]: 'Start Location',
                        df.columns[7]: 'End Location'
                    })
                    data = df.iloc[1:].values.tolist()
                    for j, row in enumerate(data):
                        trip_data = dict(zip(df.columns, row))
                        try:
                            start_time = pd.to_datetime(trip_data["Start Time"], format='%H:%M:%S', errors='coerce')
                            end_time = pd.to_datetime(trip_data["End Time"], format='%H:%M:%S', errors='coerce')
                            if pd.notna(start_time) and pd.notna(end_time):
                                trip_data["Start Time"] = start_time.strftime("%H:%M:%S")
                                trip_data["End Time"] = end_time.strftime("%H:%M:%S")
                            else:
                                logging.warning(f"Could not convert time for row {j+1} in table {i+1}. Skipping row.")
                                continue

                        except (KeyError, ValueError, AttributeError) as e:
                            logging.error(f"Error converting time for row {j+1} in table {i+1}: {e}. Skipping row.")
                            continue

                        all_data.append(trip_data)
                else:
                    logging.warning(f"No data found in table {i+1}. Skipping table.")
            return all_data
        elif file_type == "csv":
            try:
                df = pd.read_csv(file_path)
                required_cols = ['Vehicle Plate Number', 'Trip State', 'Start Time', 'End Time', 'Mileage (km)', 'Duration', 'Start Location', 'End Location']
                if not all(col in df.columns for col in required_cols):
                    raise ValueError(f"CSV file is missing required columns: {set(required_cols) - set(df.columns)}")
                return df.to_dict('records')
            except pd.errors.EmptyDataError:
                logging.error(f"Error: CSV file is empty.")
                return []
            except pd.errors.ParserError:
                logging.error(f"Error: Could not parse CSV file.")
                return []
            except KeyError as e:
                logging.error(f"Error: Missing column in CSV file: {e}")
                return []
            except ValueError as e:
                logging.error(f"Error: {e}")
                return []
        else:
            raise ValueError("Unsupported file type")
    except FileNotFoundError:
        logging.error(f"Error: File not found at {file_path}")
        return []
    except Exception as e:
        logging.exception(f"An unexpected error occurred while parsing the file: {e}")
        return []
