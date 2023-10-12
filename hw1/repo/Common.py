import datetime as dt


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
