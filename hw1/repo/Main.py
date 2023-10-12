import datetime as dt

from Common import convert_to_datetime_format
from DirectAPIClient import DirectAPIClient
from HighLevelAPIClient import HighLevelAPIClient

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


def get_user_parameters():
    user_parameters = input("Enter weather parameters (comma-separated): ")
    return [param.strip("[]\"' ") for param in user_parameters.split(',')]


def get_date_input(prompt):
    date_str = input(prompt)
    return convert_to_datetime_format(date_str)


def main():
    user_input = input("Enter 'list' to see available parameters or press Enter to continue: ")

    if user_input.lower() == 'list':
        print("Available parameters:")
        for parameter, description in parameter_descriptions.items():
            print(f"{parameter}: {description}")
        print("")

    user_input = input("Enter 'meteomatics' to use the high-level API client with the meteomatics library "
                       "or enter 'requests' to use the requests module: ")

    username = input("Enter your Meteomatics API username: ")
    password = input("Enter your Meteomatics API password: ")
    lat = float(input("Enter latitude: "))
    lon = float(input("Enter longitude: "))
    coordinates = [(lat, lon)]

    if user_input.lower() == 'meteomatics':
        user_parameters = get_user_parameters()
        startdate = get_date_input("Enter start date and time (e.g., 2023-10-05 00:00:00): ")
        enddate = get_date_input("Enter end date and time (e.g., 2023-10-16 00:00:00): ")
        hours = int(input("Enter data interval in hours: "))
        interval = dt.timedelta(hours=hours)
        client = HighLevelAPIClient(username, password)
        client.query_meteomatics_data(coordinates, user_parameters, startdate, enddate, interval)
    elif user_input.lower() == 'requests':
        user_parameters = get_user_parameters()
        startdate = get_date_input("Enter start date and time (e.g., 2023-10-05 00:00:00): ")
        enddate = get_date_input("Enter end date and time (e.g., 2023-10-16 00:00:00): ")
        interval = int(input("Enter data interval in hours: "))
        client = DirectAPIClient(username, password)
        client.query_meteomatics_data_requests(coordinates, user_parameters, startdate, enddate, interval)
    else:
        print("Invalid input. Please enter 'meteomatics' or 'requests' to choose the API client.")


if __name__ == "__main__":
    main()
