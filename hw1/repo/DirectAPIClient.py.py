import pandas as pd
import plotly.express as px
import requests

username = "sapienza_ansarifard_ashkan"
password = "WPDg43z3Mv"

coordinates = "41.902782,12.496366"
parameters = "t_2m:C"

time = "2023-10-06T00:00:00Z--2023-10-08T00:00:00Z:PT1H"

format_option = "json"

api_url = f"https://api.meteomatics.com/{time}/{parameters}/{coordinates}/{format_option}"
response = requests.get(api_url, auth=(username, password))

if response.status_code == 200:
    try:
        # Parse the JSON response
        data = response.json()

        # Extract the time series data
        time_series = data['data'][0]['coordinates'][0]['dates']

        # Create a list of dictionaries for easier DataFrame creation
        data_list = [{'time': entry['date'], 'temperature': entry['value']} for entry in time_series]

        # Create a DataFrame
        df = pd.DataFrame(data_list)

        # Convert the 'time' column to datetime
        df['time'] = pd.to_datetime(df['time'])

        # Plot the data using Plotly
        fig = px.line(df, x='time', y='temperature',
                      labels={'time': 'Time', 'temperature': 'Temperature (°C)'},
                      title="Temperature Forecast for Your Location Over 24 Hours")
        fig.show()
    except Exception as e:
        print("Failed to parse and plot data:", str(e))
else:
    if response.status_code == 100:
        print("Continue: Handshake/Authorization")
    elif response.status_code == 206:
        print("Partial Content: Further clarification about data availability.")
    elif response.status_code == 400:
        print("Bad Request: Check the URL for errors.")
    elif response.status_code == 401:
        print("Unauthorized: Check your username and password.")
    elif response.status_code == 402:
        print("Payment Required: Check payment status.")
    elif response.status_code == 403:
        print("Forbidden: Access to the API is not allowed.")
    elif response.status_code == 404:
        print("Not Found: The requested resource was not found.")
    elif response.status_code == 408:
        print("Request Time-Out: The request took too long.")
    elif response.status_code == 413:
        print("Request Entity Too Large: Too much data queried.")
    elif response.status_code == 414:
        print("Request-URI Too Large: Try a shorter URI.")
    elif response.status_code == 429:
        print("Too Many Requests: API request limit reached.")
    elif response.status_code == 500:
        print("Internal Server Error: There was an internal server error.")
    elif response.status_code == 501:
        print("Not Implemented: The requested feature is not implemented.")
    elif response.status_code == 503:
        print("Service Unavailable: The service is temporarily unavailable.")
    elif response.status_code == 504:
        print("Gateway Time-Out: The gateway didn't respond.")
    elif response.status_code == 505:
        print("HTTP version not supported: The HTTP version is not supported.")
    else:
        print(f"Failed to fetch data from the API. HTTP Error {response.status_code}: Unknown error.")
