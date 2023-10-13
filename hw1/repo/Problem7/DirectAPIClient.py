import pandas as pd
import plotly.graph_objects as go
import requests


class DirectAPIClient:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def query_meteomatics_data_requests(self, coordinates, parameters, startdate, enddate, interval,
                                        model='mix'):
        """
        Query weather data from the Meteomatics API using the requests library and plot them together in a single figure using Plotly.

        Args:
            username (str): Your Meteomatics API username.
            password (str): Your Meteomatics API password.
            coordinates (list of tuple): List of coordinates in the format [(latitude, longitude)] (1 single location per query).
            parameters (list of str): List of weather parameters to query (e.g., ['t_2m:C', 'precip_1h:mm', 'wind_speed_10m:ms'] 10 parameters with one query).
            startdate (datetime): Start date and time for the query.
            enddate (datetime): End date and time for the query.
            interval (timedelta): Time interval between data points.
            model (str): Weather model to use (default is 'mix').

        Returns:
            None
        """
        try:
            # Format the time range
            time_range = f"{startdate:%Y-%m-%dT%H:%M:%SZ}--{enddate:%Y-%m-%dT%H:%M:%SZ}:PT{interval}H"
            # Construct the API URL
            api_url = f"https://api.meteomatics.com/{time_range}/{','.join(parameters)}/{coordinates[0][0]},{coordinates[0][1]}/json"

            # Send an HTTP GET request with authentication
            response = requests.get(api_url, auth=(self.username, self.password))

            if response.status_code == 200:
                # Parse the JSON response
                data = response.json()

                # Create a Plotly figure
                fig = go.Figure()

                i = 0
                for parameter in parameters:
                    time_series = data['data'][i]['coordinates'][0]['dates']
                    data_list = [{'time': entry['date'], parameter: entry['value']} for entry in time_series]
                    df = pd.DataFrame(data_list)
                    df['time'] = pd.to_datetime(df['time'])
                    fig.add_trace(go.Scatter(x=df['time'], y=df[parameter], mode='lines', name=parameter))
                    i += 1

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
            print("Failed to query or plot data:", str(e))
