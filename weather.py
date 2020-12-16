import requests, json

def get_weather():
    api_key = "d946f58d1732625bd819026dc87b70b0"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_name = "Tartu"
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name

    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        e = x["wind"]
        celsius = round(current_temperature - 273.15)
        z = x["weather"]
        weather_description = z[0]["description"]
        wind = e["speed"]
        result = []
        result += [celsius]
        result += [weather_description]
        result += [wind]
    return result