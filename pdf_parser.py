import PyPDF2
import pandas as pd
import re
import os
from constants import CSV_COLUMNS
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI
from dotenv import load_dotenv

load_dotenv()

def extract_trip_data(file_path, file_type):
    if file_type == "pdf":
        return extract_data_from_pdf(file_path)
    elif file_type == "csv":
        return extract_data_from_csv(file_path)
    else:
        raise ValueError("Unsupported file type. Please upload a PDF or CSV file.")

def extract_data_from_pdf(file_path):
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL")
    api_url = os.getenv("OPENAI_API_URL")

    llm = OpenAI(temperature=0, openai_api_key=api_key, model_name=model, openai_api_base=api_url)
    agent = create_csv_agent(llm, file_path, verbose=True)

    prompt = (
        "Extract the following fields from the PDF as a list of records:\n"
        "1. Start Location\n"
        "2. End Location\n"
        "3. Start Time\n"
        "4. End Time\n"
        "5. Mileage (km)\n"
        "6. Duration\n"
    )

    response = agent.run(prompt)

    trip_data = []
    for record in response:
        trip_data.append({
            "Start Location": record["Start Location"],
            "End Location": record["End Location"],
            "Start Time": record["Start Time"],
            "End Time": record["End Time"],
            "Mileage (km)": float(record["Mileage (km)"].replace(',', '')),
            "Duration": record["Duration"]
        })

    return trip_data

def extract_data_from_csv(file_path):
    df = pd.read_csv(file_path)

    if not set(CSV_COLUMNS).issubset(df.columns):
        missing_columns = set(CSV_COLUMNS) - set(df.columns)
        raise ValueError(f"CSV file is missing required columns: {missing_columns}")

    trip_data = df.to_dict(orient="records")

    return trip_data
