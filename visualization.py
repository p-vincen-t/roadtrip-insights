import plotly.express as px
import pandas as pd
import json

with open('data/sample_data.json') as f:
    sample_data = json.load(f)

def create_financial_chart(data=None):
    if data is None or not data:
        data = sample_data["financial_data"]

    df = pd.DataFrame(data, columns=["Date", "Vehicle", "Category", "Amount"])
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)

    daily_data = df.resample("D").sum()

    fig = px.bar(
        daily_data,
        x=daily_data.index,
        y="Amount",
        title="Daily Income and Expenses",
        labels={"Amount": "Amount ", "index": "Date"},
        color_discrete_sequence=["#1f77b4"]
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Amount ",
        xaxis=dict(
            tickformat="%Y-%m-%d",
            dtick="D1"
        ),
        yaxis=dict(
            tickformat="$",
            tickprefix="$"
        ),
        title=dict(
            x=0.5,
            xanchor="center"
        )
    )

    return fig

def create_trip_timeline(data=None):
    if data is None or not data:
        data = sample_data["trip_data"]

    if not data:
        return None

    df = pd.DataFrame(data)
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["End Time"] = pd.to_datetime(df["End Time"])

    fig = px.timeline(
        df,
        x_start="Start Time",
        x_end="End Time",
        y="Trip State",
        color="Trip State",
        title="Trip Timeline",
        labels={"Trip State": "Trip State"}
    )

    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Trip State",
        title=dict(
            x=0.5,
            xanchor="center"
        )
    )

    return fig

def create_trip_summary(data=None):
    if data is None or not data:
        data = sample_data["trip_data"]

    if not data:
        return pd.DataFrame()

    df = pd.DataFrame(data)
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["End Time"] = pd.to_datetime(df["End Time"])
    df["Duration"] = pd.to_timedelta(df["Duration"])

    df["Trip Duration (hours)"] = df["Duration"].dt.total_seconds() / 3600.0
    df["Average Speed (km/h)"] = df["Mileage (km)"] / df["Trip Duration (hours)"]

    summary_columns = [
        "Vehicle Plate Number", "Trip State", "Start Time", "End Time",
        "Mileage (km)", "Trip Duration (hours)", "Average Speed (km/h)",
        "Start Location", "End Location"
    ]

    return df[summary_columns]

def create_daily_trip_mileage_chart(data=None):
    if data is None:
        data = pd.DataFrame(sample_data["trip_data"])

    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)

    if data.empty:
        return None

    data["_time"] = pd.to_datetime(data["_time"])
    data.set_index("_time", inplace=True)

    daily_data = data.resample("D").sum()

    fig = px.bar(
        daily_data,
        x=daily_data.index,
        y=["Trip Count", "Mileage (km)"],
        title="Daily Trip Count vs. Mileage",
        labels={"index": "Date", "value": "Count/Mileage"},
        barmode="group"
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Count/Mileage",
        xaxis=dict(
            tickformat="%Y-%m-%d",
            dtick="D1"
        ),
        yaxis=dict(
            tickformat=",.2f"
        ),
        title=dict(
            x=0.5,
            xanchor="center"
        )
    )

    return fig

def create_expense_vs_revenue_chart(data=None):
    if data is None or not data:
        data = sample_data["financial_data"]

    df = pd.DataFrame(data, columns=["Date", "Vehicle", "Category", "Amount"])
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)

    monthly_data = df.resample("M").sum()

    fig = px.bar(
        monthly_data,
        x=monthly_data.index,
        y="Amount",
        title="Monthly Income and Expenses",
        labels={"Amount": "Amount (USD)", "index": "Month"},
        color_discrete_sequence=["#1f77b4"]
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Amount (USD)",
        xaxis=dict(
            tickformat="%b %Y",
            dtick="M1"
        ),
        yaxis=dict(
            tickformat="$",
            tickprefix="$"
        ),
        title=dict(
            x=0.5,
            xanchor="center"
        )
    )

    return fig

def create_trip_efficiency_chart(data=None):
    if data is None or not data:
        data = sample_data["trip_data"]

    if not data:
        return None

    df = pd.DataFrame(data)
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["End Time"] = pd.to_datetime(df["End Time"])
    df["Duration"] = pd.to_timedelta(df["Duration"])

    df["Trip Duration (hours)"] = df["Duration"].dt.total_seconds() / 3600.0
    df["Average Speed (km/h)"] = df["Mileage (km)"] / df["Trip Duration (hours)"]
    df["Fuel Consumption (km/l)"] = df["Mileage (km)"] / df["Fuel (l)"]

    fig = px.scatter(
        df,
        x="Mileage (km)",
        y="Fuel Consumption (km/l)",
        color="Vehicle Plate Number",
        title="Trip Efficiency Metrics",
        labels={"Mileage (km)": "Mileage (km)", "Fuel Consumption (km/l)": "Fuel Consumption (km/l)"},
        hover_data=["Start Time", "End Time", "Trip Duration (hours)", "Average Speed (km/h)"]
    )

    fig.update_layout(
        xaxis_title="Mileage (km)",
        yaxis_title="Fuel Consumption (km/l)",
        title=dict(
            x=0.5,
            xanchor="center"
        )
    )

    return fig

def create_expense_forecast_chart(data=None):
    if data is None or not data:
        data = sample_data["financial_data"]

    df = pd.DataFrame(data, columns=["Date", "Vehicle", "Category", "Amount"])
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)

    monthly_data = df.resample("M").sum()

    fig = px.line(
        monthly_data,
        x=monthly_data.index,
        y="Amount",
        title="Expense Forecasting",
        labels={"Amount": "Amount (USD)", "index": "Month"},
        color_discrete_sequence=["#1f77b4"]
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Amount (USD)",
        xaxis=dict(
            tickformat="%b %Y",
            dtick="M1"
        ),
        yaxis=dict(
            tickformat="$",
            tickprefix="$"
        ),
        title=dict(
            x=0.5,
            xanchor="center"
        )
    )

    return fig
