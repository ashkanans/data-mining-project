# Weather Data Visualization App

This Python application allows you to query and visualize weather data using the Meteomatics API and Plotly. You can
specify the location, weather parameters, start date, end date, and data interval to create interactive plots of weather
data.

## Prerequisites

Before you can run this application, ensure that you have the following installed:

- Python 3.x
- Required Python packages: `meteomatics`, `plotly`

You also need a valid Meteomatics API username and password. If you don't have one, you can sign up for an account on
the [Meteomatics website](https://www.meteomatics.com).

## Installation

1. Clone or download the repository containing the Python script.

2. Install the required Python packages using pip:

## Usage

Follow these steps to run the Weather Data Visualization App:

1. Open a terminal or command prompt.

2. Navigate to the directory where you have saved the Python script.

3. Run the script using Python:

4. The application will prompt you for input. You can choose to list available weather parameters or proceed with data
   retrieval and visualization.

- To list available parameters, type `list` and press Enter.

- To proceed with data retrieval and visualization, provide the following information:

    - Meteomatics API username and password.
    - Latitude and longitude coordinates for the location of interest.
    - Weather parameters you want to query (comma-separated).
    - Start date and time in the format `YYYY-MM-DD HH:MM:SS`.
    - End date and time in the format `YYYY-MM-DD HH:MM:SS`.
    - Data interval in hours (e.g., 1, 3, 6, 24).

5. After providing the required input, the application will query the Meteomatics API and create an interactive plot of
   the specified weather parameters using Plotly. The plot will be displayed in your default web browser.

6. You can interact with the plot, zoom in/out, and hover over data points to view details.

7. Close the plot window when you are done.

## Example

Here's an example of how to use the application:

1. Run the script as mentioned above.

2. Type `list` to see available weather parameters.

3. Enter your Meteomatics API username and password when prompted.

4. Enter latitude and longitude coordinates (e.g., 41.902782 and 12.496366 for Rome).

5. Enter weather parameters (e.g., 't_2m:C,precip_1h:mm,wind_speed_10m:ms').

6. Enter start date and time (e.g., '2023-10-05 00:00:00').

7. Enter end date and time (e.g., '2023-10-16 00:00:00').

8. Enter data interval in hours (e.g., 1).

9. The application will query and visualize the selected weather data.

10. Interact with the plot as needed and close the plot window when done.

## Author

This Weather Data Visualization App was created by Ashkan Ansarifard.