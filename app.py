import streamlit as st
import pandas as pd
from db_manager import DBManager
from pdf_parser import extract_trip_data
from visualization import create_financial_chart, create_trip_timeline, create_trip_summary, create_daily_trip_mileage_chart
import datetime

db_manager = DBManager()

st.title("RoadTrip Insights")

# Daily Income and Expense Management Section
st.header("Daily Income and Expenses")
date = st.date_input("Date")
category = st.selectbox("Category", ["Revenue", "Fuel costs", "Repair costs", "Spare parts costs"])
amount = st.number_input("Amount")

if st.button("Add Entry"):
    if date and category and amount:
        db_manager.insert_daily_data(date.strftime("%Y-%m-%d"), category, amount)
        st.success("Entry added successfully!")
    else:
        st.error("Please fill all fields.")

daily_data = db_manager.get_daily_data()
if daily_data:
    fig = create_financial_chart(daily_data)
    st.plotly_chart(fig)

# Trip Data Handling Section
st.header("Trip Data Upload")
file_type = st.radio("Choose file type", ["CSV", "PDF"], index=0)
uploaded_file = st.file_uploader("Choose a file", type=["pdf", "csv"])

if file_type == "CSV":
    st.markdown("**Expected CSV Header Titles:** Vehicle Plate Number, Trip State, Start Time, End Time, Mileage (km), Duration, Start Location, End Location")

if uploaded_file is not None:
    try:
        with open("temp_file", "wb") as f:
            f.write(uploaded_file.read())
        if file_type == "PDF":
            file_type = "pdf"
        elif file_type == "CSV":
            file_type = "csv"
        else:
            st.error("Unsupported file type. Please upload a PDF or CSV file.")
            file_type = None

        if file_type:
            trip_data = extract_trip_data("temp_file", file_type)
            if trip_data:
                db_manager.write_influx_data(trip_data)
                st.success("Trip data uploaded successfully!")
                trip_summary = create_trip_summary(trip_data)
                st.dataframe(trip_summary)
                fig = create_trip_timeline(trip_data)
                if fig:
                    st.plotly_chart(fig)
                else:
                    st.error("Could not generate trip timeline. Check file format.")
            else:
                #Display specific error message for missing columns
                if "Error: CSV file is missing required columns:" in str(trip_data):
                    st.error(str(trip_data))
                else:
                    st.error("Could not extract trip data from the file.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

#Add button to clear InfluxDB data
if st.button("Clear Trip Data"):
    if db_manager.clear_influxdb_data():
        st.success("InfluxDB data cleared successfully!")
    else:
        st.error("Error clearing InfluxDB data.")

#Add visualization from InfluxDB data
st.header("Trip Data Analysis")
daily_trip_data = db_manager.get_daily_trip_data()
if daily_trip_data is not None:
    fig = create_daily_trip_mileage_chart(daily_trip_data)
    if fig:
        st.plotly_chart(fig)
    else:
        st.info("No trip data available for visualization.")

db_manager.close_influx_connection()
