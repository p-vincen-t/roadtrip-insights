import plotly.express as px
import pandas as pd

def create_financial_chart(daily_data: list):
    df = pd.DataFrame(daily_data, columns=['date', 'category', 'amount'])
    # Group data by category and sum amounts
    category_sums = df.groupby('category')['amount'].sum().reset_index()
    fig = px.bar(category_sums, x='category', y='amount', title='Daily Income and Expenses by Category',
                 color='category', color_discrete_sequence=px.colors.qualitative.Pastel) #Use Pastel color palette
    return fig

def create_trip_timeline(trip_data: list):
    df = pd.DataFrame(trip_data)
    #Handle potential variations in column names
    x_start_col = next((col for col in df.columns if 'Start Time' in col), None)
    x_end_col = next((col for col in df.columns if 'End Time' in col), None)
    y_col = next((col for col in df.columns if 'Start Location' in col), None)

    if x_start_col and x_end_col and y_col:
        fig = px.timeline(df, x_start=x_start_col, x_end=x_end_col, y=y_col, title='Trip Timeline')
        return fig
    else:
        return None

def create_trip_summary(trip_data: list):
    df = pd.DataFrame(trip_data)
    return df

def create_daily_trip_mileage_chart(daily_trip_data):
    if daily_trip_data.empty:
        return None

    daily_trip_data['date'] = pd.to_datetime(daily_trip_data['date']).dt.date
    daily_summary = daily_trip_data.groupby('date').agg({'Mileage (km)': 'sum', 'Vehicle Plate Number': 'count'}).reset_index()
    daily_summary = daily_summary.rename(columns={'Vehicle Plate Number': 'Trip Count'})
    fig = px.scatter(daily_summary, x='Trip Count', y='Mileage (km)', title='Daily Trip Count vs. Total Mileage',
                     hover_data=['date'])
    return fig
