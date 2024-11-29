import streamlit as st
import pandas as pd
from db_manager import DBManager
from pdf_parser import extract_trip_data
from visualization import create_financial_chart, create_trip_timeline, create_trip_summary, create_daily_trip_mileage_chart, create_expense_vs_revenue_chart, create_trip_efficiency_chart, create_expense_forecast_chart
import datetime
from session import authenticate_user, has_permission

db_manager = DBManager()

st.session_state["authenticated"], st.session_state["role"] = authenticate_user()

if not st.session_state.get("authenticated", False):
    st.error("Authentication failed. Please try again.")
else:
    st.title("RoadTrip Insights")

    tabs = st.tabs(["Cashflow Tracking", "GPS Reporting", "Analysis", "Management"])

    with tabs[0]:
        if has_permission(st.session_state.get("role", "user"), "Cashflow Tracking"):
            st.header("Daily Income and Expenses")
            date = st.date_input("Date")
            vehicle = st.selectbox("Vehicle", [vehicle[1] for vehicle in db_manager.list_vehicles()])
            category = st.selectbox("Category", ["Revenue", "Fuel costs", "Repair costs", "Spare parts costs", "Maintenance", "Tolls", "Driver Allowance", "Insurance", "Permits"])
            amount = st.number_input("Amount", min_value=0, step=100, format="%d")

            if st.button("Add Entry"):
                if date and vehicle and category and amount:
                    db_manager.insert_daily_data(date.strftime("%Y-%m-%d"), vehicle, category, amount)
                    st.success("Entry added successfully!")
                else:
                    st.error("Please fill all fields.")

            daily_data = db_manager.get_daily_data()
            if daily_data:
                fig = create_financial_chart(daily_data)
                st.plotly_chart(fig)

                if st.button("Export Financial Report as Image"):
                    fig.write_image("financial_report.png")
                    st.success("Financial report exported as image successfully!")
        else:
            st.error("You do not have permission to access this section.")

    with tabs[1]:
        if has_permission(st.session_state.get("role", "user"), "GPS Reporting"):
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
                            if "Error: CSV file is missing required columns:" in str(trip_data):
                                st.error(str(trip_data))
                            else:
                                st.error("Could not extract trip data from the file.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.error("You do not have permission to access this section.")

    with tabs[2]:
        if has_permission(st.session_state.get("role", "user"), "Analysis"):
            st.header("Trip Data Analysis")
            daily_trip_data = db_manager.get_daily_trip_data()
            if daily_trip_data is not None:
                fig = create_daily_trip_mileage_chart(daily_trip_data)
                if fig:
                    st.plotly_chart(fig)
                else:
                    st.info("No trip data available for visualization.")
        else:
            st.error("You do not have permission to access this section.")

    with tabs[2]:
        if has_permission(st.session_state.get("role", "user"), "Analysis"):
            st.header("Data Analysis")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Expense vs Revenue Analysis")
                expense_vs_revenue_data = db_manager.get_daily_data()
                if expense_vs_revenue_data:
                    fig = create_expense_vs_revenue_chart(expense_vs_revenue_data)
                    st.plotly_chart(fig)

            with col2:
                st.subheader("Trip Efficiency Metrics")
                trip_efficiency_data = db_manager.get_daily_trip_data()
                if trip_efficiency_data:
                    fig = create_trip_efficiency_chart(trip_efficiency_data)
                    st.plotly_chart(fig)

            st.subheader("Expense Forecasting")
            expense_forecast_data = db_manager.get_daily_data()
            if expense_forecast_data:
                fig = create_expense_forecast_chart(expense_forecast_data)
                st.plotly_chart(fig)
        else:
            st.error("You do not have permission to access this section.")

    with tabs[3]:
        if has_permission(st.session_state.get("role", "user"), "Management"):
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
        else:
            st.error("You do not have permission to access this section.")

    st.sidebar.header("Reset")

    if has_permission(st.session_state.get("role", "user"), "Reset"):
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
    else:
        st.sidebar.error("You do not have permission to access this section.")

db_manager.close_influx_connection()
