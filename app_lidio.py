# import necessary libraries
import os
import pandas as pd
from flask import Flask, render_template, jsonify

# Flask Setup
app = Flask(__name__)

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

# Query the database and send the jsonified results
@app.route("/tourism")
def tourism():
    df = pd.read_csv('db/tourism_cleaned.csv')
    return df.to_json(orient='records')

if __name__ == "__main__":
    app.run()
