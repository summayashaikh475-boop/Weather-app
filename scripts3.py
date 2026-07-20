import matplotlib.pyplot as plt
import tkinter as tk
import requests
from dotenv import load_dotenv
from datetime import datetime
import os

dates = []
temps = []
feels = []
humidities = []

load_dotenv()
API_KEY = os.getenv("API_KEY")

def get_suggestion(temp, feels_like, humidity, description):
    if "rain" in description:
        return "🌧️Carry an umbrella"
    elif humidity > 80:
        return "💧Very humid, you may feel uncomfortable"
    elif temp > 30:
        return "🥤Stay hydrated"
    elif temp < 10:
        return "🧥Wear warm clothes"
    elif feels_like > temp:
        return "🥵Feels warmer due to humidity"
    elif feels_like < temp:
        return "🥶Feels cooler due to wind"
    else:
        return "😌Weather looks normal"

def get_weather():
    city = city_entry.get().strip().title()

    if city == "":
        result_label.config(text="⚠️Please enter a city")
        return
    
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

    try:
        response  = requests.get(url)
        data = response.json()
    except:
        result_label.config(text="❌ Network error")   
        return 

    if data.get("cod") != "200":
        result_label.config(text="City not found")
        return
    
    forecast_list = data.get("list", [])


    dates.clear()
    temps.clear()
    feels.clear()
    humidities.clear()


    for item in forecast_list:
        date_time = item.get("dt_txt")

        if "12:00:00" in date_time:
            date_only = date_time.split()[0]

            formatted_date = datetime.strptime(date_only, "%Y-%m-%d").strftime("%d %b")

            main = item.get("main", {})
            temp = main.get("temp")
            feel = main.get("feels_like")
            humidity = main.get("humidity")

            dates.append(date_only)
            temps.append(temp)
            feels.append(feel)
            humidities.append(humidity)

        if len(dates) == 5:
            break    

    first = forecast_list[0]
    temp = first.get("main", {}).get("temp")
    feels_like = first.get("main", {}).get("feels_like")
    humidity = first.get("main", {}).get("humidity")
    desc = first.get("weather")[0].get("description")

    if "rain" in desc:
        emoji = "🌧️"
    elif "cloud" in desc:
        emoji = "☁️"
    elif "clear" in desc:
        emoji = "☀️"
    else:
        emoji = "👌"     

    if temps[-1] > temps[0]:
        trend = "Rising temperature"
    elif temps[-1] < temps[0]:
        trend = "Falling temperature"
    else:
        trend = "⚓ Stable temperature"       

    suggestion = get_suggestion(temp, feels_like, humidity, desc)
        
    save_history(city, temp, humidity, desc)


    result = (
        f"🏙️City: {city}\n"
        f"🌡️Temp: {temp}°C\n"
        f"🤔feels like:{feels_like}°C\n"
        f"💧Humidity: {humidity}%\n"
        f"🟢Condition: {desc}\n"
        f"{trend}\n"
        f"🗣️Suggestion: {suggestion}"
    ) 
    result_label.config(text=result) 

def save_history(city, temp, humidity, desc):
    now = datetime.now()
    formatted_time = now.strftime("%A, %d %B %Y %I:%M %p")

    with open("history.txt", "a") as f:
        f.write(f"{formatted_time} | {city} | {temp}°C | {humidity}% | {desc}\n")        

def show_history():
    try:
        with open("history.txt", "r") as f:
            content = f.read()

        if content.strip() == "":
            result_label.config(text="No history found")
        else:
            result_label.config(text=content)

    except FileNotFoundError:
        result_label.config(text="No history file found")                

def show_graph():
    if not dates or not temps:
        result_label.config(text="No data available. Click Get Weather first.")
        return
    
    plt.figure()
    plt.plot(dates, temps, marker='o', label="Temperature")
    plt.plot(dates, feels, marker='o', linestyle='--', label="Feels Like")
    plt.plot(dates, humidities, marker='s', label="Humidity (%)")

    plt.title(f"5-Day Forecast for {city_entry.get()}")
    plt.xlabel("Dates")
    plt.ylabel("Temperature (°C)")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("forecast.png")
    plt.show()

root = tk.Tk()
root.title("Weather App")
root.geometry("400x400")

city_entry = tk.Entry(root, width=25, font=("Arial", 14))
city_entry.pack(pady=15)

btn = tk.Button(root, text="Get Weather", command=get_weather)
btn.pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 12), justify="left")
result_label.pack(pady=20)

graph_btn = tk.Button(root, text="Show Graph", command=show_graph)
graph_btn.pack(pady=10)

history_btn = tk.Button(root, text="View History", command=show_history)
history_btn.pack(pady=5)

root.mainloop()