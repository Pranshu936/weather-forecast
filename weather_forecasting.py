#padh le salle
import requests
import json
import os
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog, messagebox

class WeatherApp:
    def __init__(self, api_key, filename='favorite_cities.json'):
        """
        Initialize the WeatherApp with an API key and optional filename for favorites.
        """
        self.api_key = api_key
        self.filename = filename
        self.base_url = "http://api.openweathermap.org/data/2.5/weather?"
        self.forecast_url = "http://api.openweathermap.org/data/2.5/forecast?"
        self.favorite_cities = []
        self.load_favorites()  # Load favorite cities from the file

    def load_favorites(self):
        """
        Load the list of favorite cities from a JSON file if it exists.
        """
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.favorite_cities = json.load(f)

    def save_favorites(self):
        """
        Save the list of favorite cities to a JSON file.
        """
        with open(self.filename, 'w') as f:
            json.dump(self.favorite_cities, f)

    def get_weather(self, city):
        """
        Fetch the current weather data for a given city using the OpenWeatherMap API.
        """
        complete_url = self.base_url + "appid=" + self.api_key + "&q=" + city
        response = requests.get(complete_url)
        return response.json()

    def get_forecast(self, city):
        """
        Fetch the 5-day weather forecast for a given city using the OpenWeatherMap API.
        """
        complete_url = self.forecast_url + "appid=" + self.api_key + "&q=" + city
        response = requests.get(complete_url)
        return response.json()

    def display_weather(self, weather_data):
        """
        Display current weather information from the fetched data.
        """
        if weather_data['cod'] != '404':
            main = weather_data['main']
            wind = weather_data['wind']
            weather = weather_data['weather'][0]
            result = (f"Temperature: {main['temp']}K\n"
                      f"Pressure: {main['pressure']} hPa\n"
                      f"Humidity: {main['humidity']}%\n"
                      f"Weather: {weather['description']}\n"
                      f"Wind Speed: {wind['speed']} m/s\n")
        else:
            result = "City not found"
        return result

    def plot_forecast(self, forecast_data):
        """
        Plot the 5-day weather forecast data using matplotlib.
        """
        if forecast_data['cod'] != '404':
            dates = [entry['dt_txt'] for entry in forecast_data['list']]
            temperatures = [entry['main']['temp'] for entry in forecast_data['list']]
            plt.figure(figsize=(10, 5))
            plt.plot(dates, temperatures, marker='o')
            plt.xlabel('Date')
            plt.ylabel('Temperature (K)')
            plt.title('5-Day Weather Forecast')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

    def add_favorite_city(self, city):
        """
        Add a city to the list of favorite cities and save it to the file.
        """
        self.favorite_cities.append(city)
        self.save_favorites()

    def show_favorite_cities(self):
        """
        Print the list of favorite cities.
        """
        for city in self.favorite_cities:
            print(city)

    def get_top_favorite_city(self):
        """
        Get the top favorite city from the list of favorite cities.
        """
        if self.favorite_cities:
            return self.favorite_cities[0]
        else:
            return None

class WeatherAppGUI:
    def __init__(self, master, app):
        """
        Initialize the GUI with a master window and the WeatherApp instance.
        """
        self.master = master
        self.app = app
        self.master.title("Weather App")
        self.create_widgets()

    def create_widgets(self):
        """
        Create and place widgets in the GUI window.
        """
        self.label = tk.Label(self.master, text="Enter City Name:")
        self.label.pack()
        self.entry = tk.Entry(self.master)
        self.entry.pack()
        self.get_weather_button = tk.Button(self.master, text="Get Weather", command=self.get_weather)
        self.get_weather_button.pack()
        self.get_forecast_button = tk.Button(self.master, text="Get 5-Day Forecast", command=self.get_forecast)
        self.get_forecast_button.pack()
        self.add_favorite_button = tk.Button(self.master, text="Add to Favorites", command=self.add_favorite)
        self.add_favorite_button.pack()
        self.show_favorites_button = tk.Button(self.master, text="Show Favorite Cities", command=self.show_favorites)
        self.show_favorites_button.pack()
        self.result_text = tk.Text(self.master, height=10, width=50)
        self.result_text.pack()

    def get_weather(self):
        """
        Fetch and display the current weather for the city entered by the user or the top favorite city.
        """
        city = self.entry.get().strip()  # Get the city name from the entry widget and remove any leading/trailing whitespace
        if not city:  # Check if no city name was entered
            city = self.app.get_top_favorite_city()  # Use the top favorite city if no city was entered
            if city is None:  # Check if there are no favorite cities
                messagebox.showerror("Error", "No city entered and no favorite cities available.")
                return
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert(tk.END, f"No city entered. Showing weather for top favorite city: {city}\n")
        weather_data = self.app.get_weather(city)
        result = self.app.display_weather(weather_data)
        self.result_text.insert(tk.END, result)

    def get_forecast(self):
        """
        Fetch and plot the 5-day weather forecast for the city entered by the user.
        """
        city = self.entry.get().strip()
        if not city:
            city = self.app.get_top_favorite_city()
            if city is None:
                messagebox.showerror("Error", "No city entered and no favorite cities available.")
                return
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert(tk.END, f"No city entered. Showing 5-day forecast for top favorite city: {city}\n")
        forecast_data = self.app.get_forecast(city)
        self.app.plot_forecast(forecast_data)

    def add_favorite(self):
        """
        Add the city entered by the user to the list of favorite cities.
        """
        city = self.entry.get().strip()
        if city:
            self.app.add_favorite_city(city)
            messagebox.showinfo("Success", f"{city} added to favorites")
        else:
            messagebox.showwarning("Warning", "No city entered. Cannot add to favorites.")

    def show_favorites(self):
        """
        Display the list of favorite cities in a message box.
        """
        favorites = "\n".join(self.app.favorite_cities)
        messagebox.showinfo("Favorite Cities", favorites)

def main():
    """
    Main function to run the application.
    """
    api_key = '8301fb4e5bbff8c15a510a57d54d01c4'  
    app = WeatherApp(api_key)  # Create an instance of the WeatherApp
    root = tk.Tk()  # Create the main window
    gui = WeatherAppGUI(root, app)  # Create the GUI
    root.mainloop()  # Start the GUI event loop

if __name__ == "__main__":
    main()
