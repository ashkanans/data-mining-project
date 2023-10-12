import meteomatics.api as api
import plotly.graph_objects as go


class HighLevelAPIClient:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def query_meteomatics_data(self, coordinates, parameters, startdate, enddate, interval, model='mix'):
        """
        Query weather data from the Meteomatics API and plot them together in a single figure using Plotly.

        Args:
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
            # Query the time series data
            df = api.query_time_series(coordinates, startdate, enddate, interval, parameters, self.username,
                                       self.password,
                                       model=model)
        except Exception as e:
            print("Failed to query the API:", str(e))
            return

        # Create a subplot with the number of rows based on the number of parameters
        fig = go.Figure()

        # Add traces for each parameter
        for parameter in parameters:
            trace_data = df[parameter]
            fig.add_trace(
                go.Scatter(x=df.index.get_level_values('validdate'), y=trace_data, mode='lines', name=parameter))

        # Update the layout
        fig.update_layout(title='Weather Data',
                          xaxis_title='Time',
                          yaxis_title='',
                          showlegend=True,
                          legend=dict(x=0, y=1),
                          barmode='stack')

        # Show the figure
        fig.show()
