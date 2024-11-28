import plotly.express as px
import pandas as pd
import json

# Load sample data
with open('data/sample_data.json') as f:
    sample_data = json.load(f)

def create_financial_chart(data=None):
    """
    Create a financial chart using the provided data.

    Parameters:
    - data (list): A list of tuples containing date, vehicle, category, and amount.

    Returns:
    - fig: A Plotly figure object.
    """
    if data is None or not data:
        data = sample_data["financial_data"]

    df = pd.DataFrame(data, columns=["Date", "Vehicle", "Category", "Amount"])
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)

    # Resample data to get daily totals
    daily_data = df.resample("D").sum()

    # Create a bar chart for daily income and expenses
    fig = px.bar(
        daily_data,
        x=daily_data.index,
        y="Amount",
        title="Daily Income and Expenses",
        labels={"Amount": "Amount ", "index": "Date"},
        color_discrete_sequence=["#1f77b4"]  # Set bar color to blue
    )

    # Customize the layout
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Amount ",
        xaxis=dict(
            tickformat="%Y-%m-%d",  # Format x-axis labels as date
            dtick="D1"  # Set x-axis ticks to daily intervals
        ),
        yaxis=dict(
            tickformat="$",  # Format y-axis labels with currency symbol
            tickprefix="$"
        ),
        title=dict(
            x=0.5,  # Center the title
            xanchor="center"
        )
    )

    return fig

def create_trip_timeline(data=None):
    """
    Create a timeline visualization for trip data.

    Parameters:
    - data (list): A list of dictionaries containing trip data.

    Returns:
    - fig: A Plotly figure object.
    """
    if data is None or not data:
        data = sample_data["trip_data"]

    if not data:
        return None

    df = pd.DataFrame(data)
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["End Time"] = pd.to_datetime(df["End Time"])

    # Create a timeline chart
    fig = px.timeline(
        df,
        x_start="Start Time",
        x_end="End Time",
        y="Trip State",
        color="Trip State",
        title="Trip Timeline",
        labels={"Trip State": "Trip State"}
    )

    # Customize the layout
    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Trip State",
        title=dict(
            x=0.5,  # Center the title
            xanchor="center"
        )
    )

    return fig

def create_trip_summary(data=None):
    """
    Create a summary table for trip data.

    Parameters:
    - data (list): A list of dictionaries containing trip data.

    Returns:
    - df: A Pandas DataFrame containing the trip summary.
    """
    if data is None or not data:
        data = sample_data["trip_data"]

    if not data:
        return pd.DataFrame()

    df = pd.DataFrame(data)
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["End Time"] = pd.to_datetime(df["End Time"])
    df["Duration"] = pd.to_timedelta(df["Duration"])

    # Calculate additional summary metrics
    df["Trip Duration (hours)"] = df["Duration"].dt.total_seconds() / 3600.0
    df["Average Speed (km/h)"] = df["Mileage (km)"] / df["Trip Duration (hours)"]

    # Select relevant columns for the summary
    summary_columns = [
        "Vehicle Plate Number", "Trip State", "Start Time", "End Time",
        "Mileage (km)", "Trip Duration (hours)", "Average Speed (km/h)",
        "Start Location", "End Location"
    ]

    return df[summary_columns]

def create_daily_trip_mileage_chart(data=None):
    """
    Create a chart showing daily trip count vs. mileage.

    Parameters:
    - data (DataFrame): A DataFrame containing trip data.

    Returns:
    - fig: A Plotly figure object.
    """
    if data is None or data.empty:
        data = pd.DataFrame(sample_data["trip_data"])

    if data is None or data.empty:
        return None

    # Ensure the data is in the correct format
    data["_time"] = pd.to_datetime(data["_time"])
    data.set_index("_time", inplace=True)

    # Resample data to get daily totals
    daily_data = data.resample("D").sum()

    # Create a bar chart for daily trip count vs. mileage
    fig = px.bar(
        daily_data,
        x=daily_data.index,
        y=["Trip Count", "Mileage (km)"],
        title="Daily Trip Count vs. Mileage",
        labels={"index": "Date", "value": "Count/Mileage"},
        barmode="group"
    )

    # Customize the layout
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Count/Mileage",
        xaxis=dict(
            tickformat="%Y-%m-%d",  # Format x-axis labels as date
            dtick="D1"  # Set x-axis ticks to daily intervals
        ),
        yaxis=dict(
            tickformat=",.2f"  # Format y-axis labels with thousand separators and 2 decimal places
        ),
        title=dict(
            x=0.5,  # Center the title
            xanchor="center"
        )
    )

    return fig

def create_expense_vs_revenue_chart(data=None):
    """
    Create a chart showing expense vs. revenue over different timeframes.

    Parameters:
    - data (list): A list of tuples containing date, vehicle, category, and amount.

    Returns:
    - fig: A Plotly figure object.
    """
    if data is None or not data:
        data = sample_data["financial_data"]

    df = pd.DataFrame(data, columns=["Date", "Vehicle", "Category", "Amount"])
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)

    # Resample data to get monthly totals
    monthly_data = df.resample("M").sum()

    # Create a bar chart for monthly income and expenses
    fig = px.bar(
        monthly_data,
        x=monthly_data.index,
        y="Amount",
        title="Monthly Income and Expenses",
        labels={"Amount": "Amount (USD)", "index": "Month"},
        color_discrete_sequence=["#1f77b4"]  # Set bar color to blue
    )

    # Customize the layout
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Amount (USD)",
        xaxis=dict(
            tickformat="%b %Y",  # Format x-axis labels as month and year
            dtick="M1"  # Set x-axis ticks to monthly intervals
        ),
        yaxis=dict(
            tickformat="$",  # Format y-axis labels with currency symbol
            tickprefix="$"
        ),
        title=dict(
            x=0.5,  # Center the title
            xanchor="center"
        )
    )

    return fig

def create_trip_efficiency_chart(data=None):
    """
    Create a chart showing trip efficiency metrics.

    Parameters:
    - data (list): A list of dictionaries containing trip data.

    Returns:
    - fig: A Plotly figure object.
    """
    if data is None or not data:
        data = sample_data["trip_data"]

    if not data:
        return None

    df = pd.DataFrame(data)
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["End Time"] = pd.to_datetime(df["End Time"])
    df["Duration"] = pd.to_timedelta(df["Duration"])

    # Calculate additional summary metrics
    df["Trip Duration (hours)"] = df["Duration"].dt.total_seconds() / 3600.0
    df["Average Speed (km/h)"] = df["Mileage (km)"] / df["Trip Duration (hours)"]
    df["Fuel Consumption (km/l)"] = df["Mileage (km)"] / df["Fuel (l)"]

    # Create a scatter plot for trip efficiency metrics
    fig = px.scatter(
        df,
        x="Mileage (km)",
        y="Fuel Consumption (km/l)",
        color="Vehicle Plate Number",
        title="Trip Efficiency Metrics",
        labels={"Mileage (km)": "Mileage (km)", "Fuel Consumption (km/l)": "Fuel Consumption (km/l)"},
        hover_data=["Start Time", "End Time", "Trip Duration (hours)", "Average Speed (km/h)"]
    )

    # Customize the layout
    fig.update_layout(
        xaxis_title="Mileage (km)",
        yaxis_title="Fuel Consumption (km/l)",
        title=dict(
            x=0.5,  # Center the title
            xanchor="center"
        )
    )

    return fig

def create_expense_forecast_chart(data=None):
    """
    Create a chart showing expense forecasting.

    Parameters:
    - data (list): A list of tuples containing date, vehicle, category, and amount.

    Returns:
    - fig: A Plotly figure object.
    """
    if data is None or not data:
        data = sample_data["financial_data"]

    df = pd.DataFrame(data, columns=["Date", "Vehicle", "Category", "Amount"])
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)

    # Resample data to get monthly totals
    monthly_data = df.resample("M").sum()

    # Create a line chart for expense forecasting
    fig = px.line(
        monthly_data,
        x=monthly_data.index,
        y="Amount",
        title="Expense Forecasting",
        labels={"Amount": "Amount (USD)", "index": "Month"},
        color_discrete_sequence=["#1f77b4"]  # Set line color to blue
    )

    # Customize the layout
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Amount (USD)",
        xaxis=dict(
            tickformat="%b %Y",  # Format x-axis labels as month and year
            dtick="M1"  # Set x-axis ticks to monthly intervals
        ),
        yaxis=dict(
            tickformat="$",  # Format y-axis labels with currency symbol
            tickprefix="$"
        ),
        title=dict(
            x=0.5,  # Center the title
            xanchor="center"
        )
    )

    return fig
