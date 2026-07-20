import requests

API_KEY = ""

city = input("Enter city name: ")

url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

response = requests.get(url)
data = response.json()

if data.get("cod") != 200:
    print("Error:", data.get("message"))
else:
    print("\nWeather Report")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    print("City:", data.get("name"))
    print("Temperature:", data.get("main", {}).get("temp"))
    print("Humidity:", data.get("main", {}).get("humidity"))

    weather = data.get("weather")
    if weather:
        print("Condition:", weather[0].get("description"))

    print("Wind speed:", data.get("wind",{}).get("speed"))    

    
    