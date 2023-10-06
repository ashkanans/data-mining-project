import datetime as dt

import meteomatics.api as api
import plotly.graph_objects as go

parameter_descriptions = {
    'wind_speed_10m:ms': 'Instantaneous wind speed at 10m above ground',
    'wind_dir_10m:d': 'Instantaneous wind direction at 10m above ground in degrees',
    'wind_gusts_10m_1h:ms': 'Wind gusts in 10 m in the previous 1h',
    'wind_gusts_10m_24h:ms': 'Wind gusts in 10 m in the previous 24h',
    't_2m:C': 'Instantaneous temperature at 2m above ground in degrees Celsius',
    't_max_2m_24h:C': 'Maximum temperature at 2m height in the previous 24h',
    't_min_2m_24h:C': 'Minimum temperature at 2m height in the previous 24h',
    'msl_pressure:hPa': 'Mean sea level pressure in hectopascal (hPa)',
    'precip_1h:mm': 'Precipitation accumulated over the past hour in millimeter',
    'precip_24h:mm': 'Precipitation accumulated over the past 24 hours in millimeter',
    'weather_symbol_1h:idx': 'Weather symbol for the past hour',
    'weather_symbol_24h:idx': 'Weather symbol for the past 24 hours',
    'uv:idx': 'UV index',
    'sunrise:sql': 'Sunrise',
    'sunset:sql': 'Sunset'
}


def query_meteomatics_data(username, password, coordinates, parameters, startdate, enddate, interval, model='mix'):
    """
    Query weather data from the Meteomatics API and plot them together in a single figure using Plotly.

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
        # Query the time series data
        df = api.query_time_series(coordinates, startdate, enddate, interval, parameters, username, password,
                                   model=model)
    except Exception as e:
        print("Failed to query the API:", str(e))
        return

    # Create a subplot with the number of rows based on the number of parameters
    num_parameters = len(parameters)
    fig = go.Figure()

    # Add traces for each parameter
    for parameter in parameters:
        trace_data = df[parameter]
        fig.add_trace(go.Scatter(x=df.index.get_level_values('validdate'), y=trace_data, mode='lines', name=parameter))

    # Update the layout
    fig.update_layout(title='Weather Data',
                      xaxis_title='Time',
                      yaxis_title='',
                      showlegend=True,
                      legend=dict(x=0, y=1),
                      barmode='stack')

    # Show the figure
    fig.show()


def convert_to_datetime_format(date_str):
    try:
        # Try to parse the input as "%Y-%m-%d %H:%M:%S"
        date = dt.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        try:
            # Try to parse the input as "%Y-%m-%d" and add time as 00:00:00
            date = dt.datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Please use either 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS'.")

    return date


if __name__ == "__main__":
    user_input = input("Enter 'list' to see available parameters or enter to continue: ")

    if user_input.lower() == 'list':
        print("Available parameters:")
        for parameter, description in parameter_descriptions.items():
            print(f"{parameter}: {description}")
        print(f"")

    # Get user input
    username = input("Enter your Meteomatics API username: ")
    password = input("Enter your Meteomatics API password: ")
    lat = float(input("Enter latitude: "))
    lon = float(input("Enter longitude: "))
    coordinates = [(lat, lon)]
    user_parameters = input("Enter weather parameters (comma-separated): ")
    cleaned_parameters = [param.strip("[]\"' ") for param in user_parameters.split(',')]

    start_date_str = input("Enter start date and time (e.g., 2023-10-05 00:00:00): ")
    end_date_str = input("Enter end date and time (e.g., 2023-10-16 00:00:00): ")

    startdate = convert_to_datetime_format(start_date_str)
    enddate = convert_to_datetime_format(end_date_str)

    interval_hours = int(input("Enter data interval in hours: "))

    interval = dt.timedelta(hours=interval_hours)

    # Query and plot weather data
    query_meteomatics_data(username, password, coordinates, cleaned_parameters, startdate, enddate, interval)
