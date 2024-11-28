import streamlit as st
import pandas as pd
from db_manager import DBManager
from pdf_parser import extract_trip_data
from visualization import create_financial_chart, create_trip_timeline, create_trip_summary, create_daily_trip_mileage_chart, create_expense_vs_revenue_chart, create_trip_efficiency_chart, create_expense_forecast_chart
import datetime

# Initialize the database manager
db_manager = DBManager()

# Set the title of the Streamlit application
st.title("RoadTrip Insights")

# Create tabs for different sections
tabs = st.tabs(["Cashflow Tracking", "GPS Reporting", "Analysis", "Management"])

# Section for Daily Income and Expense Management
with tabs[0]:
    st.header("Daily Income and Expenses")
    date = st.date_input("Date")
    vehicle = st.selectbox("Vehicle", [vehicle[1] for vehicle in db_manager.list_vehicles()])
    category = st.selectbox("Category", ["Revenue", "Fuel costs", "Repair costs", "Spare parts costs", "Maintenance", "Tolls", "Driver Allowance", "Insurance", "Permits"])
    amount = st.number_input("Amount", min_value=0, step=100, format="%d")

    # Button to add an entry to the database
    if st.button("Add Entry"):
        if date and vehicle and category and amount:
            db_manager.insert_daily_data(date.strftime("%Y-%m-%d"), vehicle, category, amount)
            st.success("Entry added successfully!")
        else:
            st.error("Please fill all fields.")

    # Retrieve and display daily financial data
    daily_data = db_manager.get_daily_data()
    if daily_data:
        fig = create_financial_chart(daily_data)
        st.plotly_chart(fig)

        # Button to export the financial report as an image
        if st.button("Export Financial Report as Image"):
            fig.write_image("financial_report.png")
            st.success("Financial report exported as image successfully!")

# Section for Trip Data Handling
with tabs[1]:
    st.header("Trip Data Upload")
    file_type = st.radio("Choose file type", ["CSV", "PDF"], index=0)
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "csv"])

    # Display expected CSV headers if CSV is selected
    if file_type == "CSV":
        st.markdown("**Expected CSV Header Titles:** Vehicle Plate Number, Trip State, Start Time, End Time, Mileage (km), Duration, Start Location, End Location")

    # Handle file upload and data extraction
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
                    # Display specific error message for missing columns
                    if "Error: CSV file is missing required columns:" in str(trip_data):
                        st.error(str(trip_data))
                    else:
                        st.error("Could not extract trip data from the file.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Section for Trip Data Analysis
with tabs[2]:
    st.header("Trip Data Analysis")
    daily_trip_data = db_manager.get_daily_trip_data()
    if daily_trip_data is not None:
        fig = create_daily_trip_mileage_chart(daily_trip_data)
        if fig:
            st.plotly_chart(fig)
        else:
            st.info("No trip data available for visualization.")

# Section for Data Analysis
with tabs[2]:
    st.header("Data Analysis")

    # Create a layout with two columns for charts
    col1, col2 = st.columns(2)

    # Expense vs Revenue Analysis
    with col1:
        st.subheader("Expense vs Revenue Analysis")
        expense_vs_revenue_data = db_manager.get_daily_data()
        if expense_vs_revenue_data:
            fig = create_expense_vs_revenue_chart(expense_vs_revenue_data)
            st.plotly_chart(fig)

    # Trip Efficiency Metrics
    with col2:
        st.subheader("Trip Efficiency Metrics")
        trip_efficiency_data = db_manager.get_daily_trip_data()
        if trip_efficiency_data:
            fig = create_trip_efficiency_chart(trip_efficiency_data)
            st.plotly_chart(fig)

    # Expense Forecasting
    st.subheader("Expense Forecasting")
    expense_forecast_data = db_manager.get_daily_data()
    if expense_forecast_data:
        fig = create_expense_forecast_chart(expense_forecast_data)
        st.plotly_chart(fig)

# Section for Vehicle Management
with tabs[3]:
    st.header("Vehicle Management")
    st.subheader("Add New Vehicle")
    plate = st.text_input("Vehicle Plate Number")
    model = st.text_input("Vehicle Model")
    if st.button("Add Vehicle"):
        if plate and model:
            db_manager.add_vehicle(plate, model)
            st.success("Vehicle added successfully!")
        else:
            st.error("Please fill all fields.")

    st.subheader("List Vehicles")
    vehicles = db_manager.list_vehicles()
    if vehicles:
        st.table(pd.DataFrame(vehicles, columns=["ID", "Plate Number", "Model"]))
    else:
        st.info("No vehicles found.")

st.sidebar.header("Reset")

if st.sidebar.button("Clear Cashflow"):
    db_manager.clear_sqlite_data()
    st.sidebar.success("Cashflow cleared successfully!")

st.sidebar.markdown('----')
st.sidebar.subheader("Clear Trips")
start_date = st.sidebar.date_input("Start Date", value=datetime.date.today() - datetime.timedelta(days=30))
end_date = st.sidebar.date_input("End Date", value=datetime.date.today())

if st.sidebar.button("Clear"):
    if db_manager.clear_influxdb_data(start_date, end_date):
        st.sidebar.success("Trips cleared successfully!")
    else:
        st.error("Error clearing InfluxDB data.")
# Close the InfluxDB connection
db_manager.close_influx_connection()
