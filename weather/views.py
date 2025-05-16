# from django.shortcuts import render
# import json
# import urllib.request


# # Create your views here.
# def index(request):
#     if request.method == 'POST':
#         city = request.POST['city']
#         res = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q='+city+'&appid=f15d5482563d7bef4785a8aa1fd04e39').read()
#         json_data = json.loads(res)
#         data = {
#             "country_code": str(json_data['sys']['country']),
#             "coordinate": str(json_data['coord']['lon']) + ' ' + str(json_data['coord']['lat']),
#             "temp": str(json_data['main']['temp'])+ 'k',
#             "pressure": str(json_data['main']['pressure']),
#             "humidity": str(json_data['main']['humidity']),        }
#     else:
#         city = ''
#         data = {}
#     return render(request,  'index.html' , {'city': city , 'data': data})

from django.shortcuts import render
import urllib.request
import urllib.parse
import json

# Create your views here.
''' This function handles the index view of the weather appication and also handels errors
                    if the city is not found or if the API request fails.'''
# it process the request and fetches weather data from the openweathermap API.
# It takes the city name from the POST request, makes an API call, and returns the weather data .

def index(request):
    weather_data = {}

    if request.method == "POST":
        city = request.POST.get('city')

        if city:
            city = city.strip()
            city_encoded = urllib.parse.quote(city)
            api_key = "f15d5482563d7bef4785a8aa1fd04e39"
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city_encoded}&units=metric&appid={api_key}"

            try:
                source = urllib.request.urlopen(url).read()
                data = json.loads(source)

                if data.get("cod") != 200:
                    weather_data = {'error': f"City '{city}' not found."}
                else:
                    weather_data = {
                        "city": city,
                        "country_code": data["sys"]["country"],
                        "coordinate": f"{data['coord']['lon']}, {data['coord']['lat']}",
                        "temp": f"{data['main']['temp']} °C",
                        "pressure": f"{data['main']['pressure']} hPa",
                        "humidity": f"{data['main']['humidity']}%",
                    }
            except Exception as e:
                weather_data = {"error": f"Request failed: {str(e)}"}

    return render(request, "index.html", {"data": weather_data})

