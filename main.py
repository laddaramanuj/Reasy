import os
import base64
import json
from flask import Flask, jsonify, request, render_template
from google.cloud import bigquery
import pandas as pd

app = Flask(__name__)

def fetch_data_from_bigquery(mis):
    service_account_path = "C:\\Users\\ladda\\Downloads\\handy-balancer-435215-t5-214cd68b8064.json"
    client = bigquery.Client.from_service_account_json(service_account_path)

    query = f"""
        SELECT * 
        FROM `handy-balancer-435215-t5.Result.civil_sem_2`
        WHERE mis = {mis}
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("mis", "STRING", str(mis))  # Ensure mis is the right type
        ]
    )

    query_job = client.query(query, job_config=job_config)  # Run the query
    df = query_job.to_dataframe()  # Convert the results to a DataFrame

    # Skip specific columns
    columns_to_skip = ['pre', 'post', 'total', 'mul', 'know', 'sr']
    df = df.loc[:, ~df.columns.isin(columns_to_skip)]  # Remove unwanted columns

    # Transpose the DataFrame
    df_transposed = df.transpose().reset_index()  # Transpose and reset index
    df_transposed.columns = df_transposed.iloc[0]  # Set first row as header
    df_transposed = df_transposed[1:]  # Remove the first row

    # Ensure all columns and values are strings to avoid JSON serialization issues
    df_transposed.columns = df_transposed.columns.astype(str)  # Convert column names to strings
    for col in df_transposed.columns:
        df_transposed[col] = df_transposed[col].astype(str)  # Convert all values to strings

    return df_transposed

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_data', methods=['POST'])
def fetch_data():
    mis = request.json['mis']  # Get MIS number from the request
    df = fetch_data_from_bigquery(mis)  # Fetch and process the data
    data = df.to_dict(orient='records')  # Convert DataFrame to records
    columns = df.columns.tolist()  # Get column names
    return jsonify({'columns': columns, 'data': data})  # Return both columns and data as JSON

if __name__ == "__main__":
    app.run(debug=True)