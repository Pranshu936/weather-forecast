import requests
import json
import os
import matplotlib.pyplot as plt
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

class WeatherApp:
    def __init__(self, api_key, filename='favorite_cities.json'):
        self.api_key = api_key
        self.filename = filename
        self.base_url = "http://api.openweathermap.org/data/2.5/weather?"
        self.forecast_url = "http://api.openweathermap.org/data/2.5/forecast?"
        self.favorite_cities = []
        self.load_favorites()

    def load_favorites(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.favorite_cities = json.load(f)

    def save_favorites(self):
        with open(self.filename, 'w') as f:
            json.dump(self.favorite_cities, f)

    def get_weather(self, city):
        complete_url = self.base_url + "appid=" + self.api_key + "&q=" + city
        response = requests.get(complete_url)
        return response.json()

    def get_forecast(self, city):
        complete_url = self.forecast_url + "appid=" + self.api_key + "&q=" + city
        response = requests.get(complete_url)
        return response.json()

    def display_weather(self, weather_data):
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
        if forecast_data['cod'] != '404':
            dates = [entry['dt_txt'] for entry in forecast_data['list']]
            temperatures = [entry['main']['temp'] for entry in forecast_data['list']]

            # Set the style for dark background
            plt.style.use('dark_background')

            plt.figure(figsize=(10, 5))
            plt.plot(dates, temperatures, marker='o')
            plt.xlabel('Date')
            plt.ylabel('Temperature (K)')
            plt.title('5-Day Weather Forecast')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

    def add_favorite_city(self, city):
        if city not in self.favorite_cities:
            self.favorite_cities.append(city)
            self.save_favorites()

    def show_favorite_cities(self):
        return self.favorite_cities

    def get_top_favorite_city(self):
        if self.favorite_cities:
            return self.favorite_cities[0]
        else:
            return None

class WeatherAppGUI:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.master.title("Weather App")
        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use('darkly')

        self.label = ttk.Label(self.master, text="Enter City Name:")
        self.label.pack(pady=10)

        self.entry = ttk.Entry(self.master, width=30)
        self.entry.pack(pady=10)

        self.get_weather_button = ttk.Button(self.master, text="Get Weather", command=self.get_weather)
        self.get_weather_button.pack(pady=5)

        self.get_forecast_button = ttk.Button(self.master, text="Get 5-Day Forecast", command=self.get_forecast)
        self.get_forecast_button.pack(pady=5)

        self.add_favorite_button = ttk.Button(self.master, text="Add to Favorites", command=self.add_favorite)
        self.add_favorite_button.pack(pady=5)

        self.show_favorites_button = ttk.Button(self.master, text="Show Favorite Cities", command=self.show_favorites)
        self.show_favorites_button.pack(pady=5)

        self.favorite_city_label = ttk.Label(self.master, text="Select Favorite City:")
        self.favorite_city_label.pack(pady=10)

        self.favorite_city_combobox = ttk.Combobox(self.master, values=self.app.show_favorite_cities())
        self.favorite_city_combobox.pack(pady=10)
        self.favorite_city_combobox.bind("<<ComboboxSelected>>", self.select_favorite_city)

        self.result_text = ttk.Text(self.master, height=10, width=50, font=('Helvetica', 12))
        self.result_text.pack(pady=10)

    def get_weather(self):
        city = self.entry.get().strip()
        if not city:
            city = self.app.get_top_favorite_city()
            if city is None:
                messagebox.showerror("Error", "No city entered and no favorite cities available.")
                return
            self.result_text.delete('1.0', 'end')
            self.result_text.insert('end', f"No city entered. Showing weather for top favorite city: {city}\n")
        weather_data = self.app.get_weather(city)
        result = self.app.display_weather(weather_data)
        self.result_text.delete('1.0', 'end')  # Clear previous info
        self.result_text.insert('end', result)

    def get_forecast(self):
        city = self.entry.get().strip()
        if not city:
            city = self.app.get_top_favorite_city()
            if city is None:
                messagebox.showerror("Error", "No city entered and no favorite cities available.")
                return
            self.result_text.delete('1.0', 'end')
            self.result_text.insert('end', f"No city entered. Showing 5-day forecast for top favorite city: {city}\n")
        forecast_data = self.app.get_forecast(city)
        self.result_text.delete('1.0', 'end')  # Clear previous info
        self.app.plot_forecast(forecast_data)

    def add_favorite(self):
        city = self.entry.get().strip()
        if city:
            self.app.add_favorite_city(city)
            self.favorite_city_combobox['values'] = self.app.show_favorite_cities()  # Update ComboBox values
            messagebox.showinfo("Success", f"{city} added to favorites")
        else:
            messagebox.showwarning("Warning", "No city entered. Cannot add to favorites.")

    def show_favorites(self):
        favorites = "\n".join(self.app.show_favorite_cities())
        messagebox.showinfo("Favorite Cities", favorites)

    def select_favorite_city(self, event):
        selected_city = self.favorite_city_combobox.get()
        if selected_city:
            self.result_text.delete('1.0', 'end')
            weather_data = self.app.get_weather(selected_city)
            result = self.app.display_weather(weather_data)
            self.result_text.insert('end', f"Weather for selected favorite city:\n{result}")

def main():
    api_key = '8301fb4e5bbff8c15a510a57d54d01c4'
    app = WeatherApp(api_key)
    root = ttk.Window(themename="darkly")
    gui = WeatherAppGUI(root, app)
    root.mainloop()

if __name__ == "__main__":
    main()
