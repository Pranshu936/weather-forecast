# Weather Application

A simple Python application that allows users to check the current weather and 5-day forecast for cities. It also provides features to add cities to a list of favorites and view weather data for those cities.

## Features

- Get current weather information for a city.
- View a 5-day weather forecast.
- Add cities to a list of favorite cities.
- View a list of favorite cities.
- Displays weather information and plots forecasts using Matplotlib.

## Requirements

- Python 3.x
- `requests` library for making API requests.
- `matplotlib` library for plotting forecasts.
- `tkinter` library for the GUI (usually included with Python).

## Setup

1. **Clone the repository**:

   ```sh
   git clone https://github.com/your-username/weather-app.git
   cd weather-app
   
2. **Install required libraries**:

If you don't have the requests and matplotlib libraries installed, you can install them using pip:

 ```sh
pip install requests matplotlib
 ```


3. **Obtain an API key**:

Sign up for an API key from OpenWeatherMap:

- Visit OpenWeatherMap API and sign up for a free account.
- Once you have an account, generate an API key from the dashboard.
4. **Configure the application**:

Open the weather_app.py file and replace the placeholder your_openweathermap_api_key_here with your actual API key.

 ```sh
api_key = 'your_openweathermap_api_key_here'
```
## Usage:
1. **Run the application**:
 ```sh
python weather_app.py
 ```
2. **Interact with the GUI**:

- Enter City Name: Type the name of the city you want to check in the text entry box.
- Get Weather: Click the "Get Weather" button to display the current weather for the entered city.
- Get 5-Day Forecast: Click the "Get 5-Day Forecast" button to plot the weather forecast for the next 5 days.
- Add to Favorites: Click the "Add to Favorites" button to add the entered city to your list of favorite cities.
- Show Favorite Cities: Click the "Show Favorite Cities" button to view the list of your favorite cities.
## File Structure
- weather_app.py: The main Python script containing the application logic and GUI.
- favorite_cities.json: A JSON file used to store the list of favorite cities (created and managed automatically).

## Acknowledgments
- OpenWeatherMap for providing the weather data API.
- Matplotlib for creating plots and visualizations.
- Tkinter for building the GUI.
