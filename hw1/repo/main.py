import requests
import pandas as pd
import plotly.express as px

username = "sapienza_ansarifard_ashkan"
password = "WPDg43z3Mv"

coordinates = "52.520551,13.461804"
parameters = "t_2m:C"

time = "2023-10-05T00:00:00Z--2023-10-08T00:00:00Z:PT1H"

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
    print("Failed to fetch data from the API.")


