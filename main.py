from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from dotenv import load_dotenv
import pandas as pd
import plotly.express as px

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_APP_KEY')


@app.route('/')
def home():
    data_deaths = pd.read_csv('./static/data/Deaths_by_Police_US.csv', index_col=0, encoding='ISO-8859-1')
    shape_deaths = data_deaths.shape
    head_deaths = data_deaths.head().to_html(classes='dataframe', index=False)

    # Plotting the number of missions per year
    data_deaths['date'] = pd.to_datetime(data_deaths['date'], format='%d/%m/%y', errors='coerce')
    data_deaths['year'] = data_deaths['date'].dt.year
    data_deaths['month'] = data_deaths['date'].dt.month
    # Count the number of deaths per month
    deaths_per_month = data_deaths.groupby(['year', 'month']).size().reset_index(name='count')
    # Create a 'year_month' column for the x-axis
    deaths_per_month['year_month'] = deaths_per_month['year'].astype(str) + '-' + deaths_per_month['month'].astype(str)
    # Create the line chart for deaths per month
    trend = px.line(deaths_per_month, x='year_month', y='count')
    trend.update_layout(xaxis_title='Year-Month', yaxis_title='Number of Deaths by Police', xaxis_tickangle=-45)
    trend.update_traces(line=dict(width=3))
    trend.update_xaxes(type='category')  # Add this line to show labels for all months
    
    # Calculate the total average deaths per month
    total_average = deaths_per_month['count'].mean()
    trend.add_hline(y=total_average, line_dash='dash', line_color='red', annotation_text=f'Total Average: {total_average:.2f}', annotation_position='top right')
    
    trend_html = trend.to_html(full_html=False)

    # Plotting number of deaths for first 10 states with px.bar
    data_deaths = data_deaths['state'].value_counts().sort_values(ascending=False)
    deaths_by_state = px.bar(data_deaths, x=data_deaths.index, y=data_deaths.values)
    deaths_by_state.update_layout(
        xaxis_title='US States',
        yaxis_title='Number of Deaths by Police',
        # yaxis=dict(type='log')
    )
    deaths_by_state_html = deaths_by_state.to_html(full_html=False)
    

    return render_template('index.html', 
                           shape_deaths=shape_deaths, 
                           head_deaths=head_deaths,
                           trend_deaths=trend_html,
                           deaths_by_state=deaths_by_state_html,
                           )


if __name__ == '__main__':
    app.run(debug=True)