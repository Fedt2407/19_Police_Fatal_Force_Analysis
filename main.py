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
                           deaths_by_state=deaths_by_state_html,
                           )


if __name__ == '__main__':
    app.run(debug=True)