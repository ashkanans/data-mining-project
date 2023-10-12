import pandas as pd
import plotly.graph_objects as go
import requests

from Common import convert_to_datetime_format

username = "sapienza_ansarifard_ashkan"
password = "WPDg43z3Mv"

coordinates = [("41.902782", "12.496366")]
parameters = "t_2m:C,sunrise:sql,sunset:sql,wind_speed_10m:ms"

startdate = convert_to_datetime_format("2023-10-11")
enddate = convert_to_datetime_format("2023-10-20")

interval = 1

try:
    # Format the time range
    time_range = f"{startdate:%Y-%m-%dT%H:%M:%SZ}--{enddate:%Y-%m-%dT%H:%M:%SZ}:PT{interval}H"
    # Construct the API URL
    api_url = f"https://api.meteomatics.com/{time_range}/{parameters}/{coordinates[0][0]},{coordinates[0][1]}/json"

    # Send an HTTP GET request with authentication
    response = requests.get(api_url, auth=(username, password))

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # Extract the time series data
        # time_series = data['data'][0]['coordinates'][0]['dates']
        #
        # # Create a list of dictionaries for easier DataFrame creation
        # data_list = [{'time': entry['date'], 'temperature': entry['value']} for entry in time_series]
        #
        # # Create a DataFrame
        # df = pd.DataFrame(data_list)
        #
        # # Convert the 'time' column to datetime
        # df['time'] = pd.to_datetime(df['time'])

        fig = go.Figure()
        # Plot the data using Plotly
        # fig = px.line(df, x='time', y='temperature',
        #               labels={'time': 'Time', 'temperature': 'Temperature (°C)'},
        #               title="Temperature Forecast for Your Location Over 24 Hours")
        # fig.add_trace(go.Scatter(x=df['time'], y=df['temperature'], mode='lines', name='temperature'))
        cleaned_parameters = [param.strip("[]\"' ") for param in parameters.split(',')]
        i = 0
        for parameter in cleaned_parameters:
            time_series = data['data'][i]['coordinates'][0]['dates']
            data_list = [{'time': entry['date'], parameter: entry['value']} for entry in time_series]
            df = pd.DataFrame(data_list)
            df['time'] = pd.to_datetime(df['time'])
            fig.add_trace(go.Scatter(x=df['time'], y=df[parameter], mode='lines', name=parameter))
            i += 1
            fig.show()

        fig.show()

    elif response.status_code == 206:
        print(f"Partial Content: Further clarification about data availability. \n{response.content}")
    elif response.status_code == 400:
        print(f"Bad Request: Check the URL for errors. \n{response.content}")
    elif response.status_code == 401:
        print(f"Unauthorized: Check your username and password. \n{response.content}")
    elif response.status_code == 402:
        print(f"Payment Required: Check payment status. \n{response.content}")
    elif response.status_code == 403:
        print(f"Forbidden: Access to the API is not allowed. \n{response.content}")
    elif response.status_code == 404:
        print(f"Not Found: The requested resource was not found.  \n{response.content}")
    elif response.status_code == 408:
        print(f"Request Time-Out: The request took too long.  \n{response.content}")
    elif response.status_code == 413:
        print(f"Request Entity Too Large: Too much data queried. \n{response.content}")
    elif response.status_code == 414:
        print(f"Request-URI Too Large: Try a shorter URI. \n{response.content}")
    elif response.status_code == 429:
        print(f"Too Many Requests: API request limit reached. \n{response.content}")
    elif response.status_code == 500:
        print(f"Internal Server Error: There was an internal server error. \n{response.content}")
    elif response.status_code == 501:
        print(f"Not Implemented: The requested feature is not implemented. \n{response.content}")
    elif response.status_code == 503:
        print(f"Service Unavailable: The service is temporarily unavailable. \n{response.content}")
    elif response.status_code == 504:
        print(f"Gateway Time-Out: The gateway didn't respond. \n{response.content}")
    elif response.status_code == 505:
        print(f"HTTP version not supported: The HTTP version is not supported. \n{response.content}")
    else:
        print(f"Failed to fetch data from the API. HTTP Error {response.status_code}: Unknown error.")
except Exception as e:
    print("Failed to query and plot data:", str(e))
