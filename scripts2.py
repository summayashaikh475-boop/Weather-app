from datetime import datetime
from dotenv import load_dotenv
import os
import requests
import matplotlib.pyplot as plt

load_dotenv()
API_KEY = os.getenv("API_KEY")


while True:
    city = input("\nEnter city name (or type 'exit' to quit): ")
    country = input("Enter country code(e.g., IN, NP, US): ")

    if city.lower() == "exit":
        print("Exiting weather app. CHEERIO!")
        break

    # CURRENT WEATHER API
    current_url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={API_KEY}&units=metric"
    current_data = requests.get(current_url).json()

    #FORECAST API
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city},{country}&appid={API_KEY}&units=metric"
    forecast_data = requests.get(forecast_url).json()

    if current_data.get("cod") != 200:
        print("Error:", current_data.get("message"))

    else:
        now = datetime.now()
        date = now.strftime("%d-%m-%y")
        time = now.strftime("%H:%M:%S")

        print("\n~~~~~~~~~~WEATHER REPORT~~~~~~~~~~")    
        print("======================================")
        print("CITY:", current_data.get("name"))
        print("COUNTRY:", current_data.get("sys", {}).get("country"))
        print("TEMPERATURE:", current_data.get("main", {}).get("temp"), "°C")
        print("HUMIDITY:", current_data.get("main", {}).get("humidity"), "%")

        weather = current_data.get("weather")
        if weather:
            print("CONDITION:", weather[0].get("description")) 

        print("WIND SPEED:", current_data.get("wind", {}).get("speed"), "m/s") 


        # SAVE HISTORY 
        with open("history.txt", "a") as file:
            weather_desc = weather[0].get("description") if weather else "N/A"

            file.write(
                f"{current_data.get("name")} | {date} {time} | "
                f"{current_data.get("main", {}).get("temp")}°C | "
                f"{weather_desc}\n"
            )

        # SUNRISE/ SUNSET
        sunrise_tms = current_data.get("sys", {}).get("sunrise")
        sunset_tms = current_data.get("sys", {}).get("sunset")

        if sunrise_tms and sunset_tms:
            sunrise_time = datetime.fromtimestamp(sunrise_tms).strftime("%H:%M:%S")
            sunset_time = datetime.fromtimestamp(sunset_tms).strftime("%H:%M:%S")

            print("SUNRISE:", sunrise_time)
            print("SUNSET:", sunset_time)


        # FORECAST (DAILY)
        print("\n 5-DAY FORECAST")
        print("======================")    

        forecast_list = forecast_data.get("list", [])
        seen_dates = set()

        dates = []
        temps = []


        for item in forecast_list:
            date_time = item.get("dt_txt")
            date_only = date_time.split()[0]

            if date_only not in seen_dates:
                seen_dates.add(date_only)

                temp = item.get("main", {}).get("temp")
                weather = item.get("weather")
                desc = weather[0].get("description") if weather else "N/A"

                print(f"{date_only} | {temp}°C | {desc}")

                # STORE FOR GRAPH
                dates.append(date_only)
                temps.append(temp)

            if len(seen_dates) == 5:
                break
            
        plt.figure()
        plt.plot(dates, temps, marker="o")

        plt.title("5-DAY TEMPERATURE FORECAST")
        plt.xlabel("Date")
        plt.ylable("Temperature(°C)")    
        plt.xticks(rotation=45)

        plt.tight_layout()
        plt.savefig("{city}_forecast.png", dpi=300)
        plt.show()