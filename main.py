from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from dotenv import load_dotenv
import pandas as pd

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_APP_KEY')


@app.route('/')
def home():
    data_deaths = pd.read_csv('./static/data/Deaths_by_Police_US.csv', index_col=0, encoding='ISO-8859-1')
    shape_deaths = data_deaths.shape
    head_deaths = data_deaths.head().to_html(classes='dataframe', index=False)

    return render_template('index.html', shape_deaths=shape_deaths, head_deaths=head_deaths)


if __name__ == '__main__':
    app.run(debug=True)