import PyPDF2
import pandas as pd
import re
from constants import CSV_COLUMNS

def extract_trip_data(file_path, file_type):
    if file_type == "pdf":
        return extract_data_from_pdf(file_path)
    elif file_type == "csv":
        return extract_data_from_csv(file_path)
    else:
        raise ValueError("Unsupported file type. Please upload a PDF or CSV file.")

def extract_data_from_pdf(file_path):
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()

    start_location_match = re.search(r"Start Location:\s*(.+)", text)
    end_location_match = re.search(r"End Location:\s*(.+)", text)
    start_time_match = re.search(r"Start Time:\s*(.+)", text)
    end_time_match = re.search(r"End Time:\s*(.+)", text)
    mileage_match = re.search(r"Mileage \(km\):\s*(.+)", text)
    duration_match = re.search(r"Duration:\s*(.+)", text)

    if not all([start_location_match, end_location_match, start_time_match, end_time_match, mileage_match, duration_match]):
        raise ValueError("PDF file is missing required fields.")

    trip_data = [
        {
            "Start Location": start_location_match.group(1).strip(),
            "End Location": end_location_match.group(1).strip(),
            "Start Time": start_time_match.group(1).strip(),
            "End Time": end_time_match.group(1).strip(),
            "Mileage (km)": float(mileage_match.group(1).strip().replace(',', '')),
            "Duration": duration_match.group(1).strip()
        }
    ]

    return trip_data

def extract_data_from_csv(file_path):
    df = pd.read_csv(file_path)

    if not set(CSV_COLUMNS).issubset(df.columns):
        missing_columns = set(CSV_COLUMNS) - set(df.columns)
        raise ValueError(f"CSV file is missing required columns: {missing_columns}")

    trip_data = df.to_dict(orient="records")

    return trip_data
