import requests
from django.shortcuts import render
from django.conf import settings

def index(request):
    weather_data = None
    error_message = None
    
    if request.method == 'POST':
        city = request.POST.get('city', '')
        
        if city:
            api_key = settings.WEATHER_API_KEY
            # Using Weatherstack API instead of OpenWeatherMap
            url = f'http://api.weatherstack.com/current?access_key={api_key}&query={city}&units=m'
            
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise exception for HTTP errors
                
                data = response.json()
                
                # Check if API returned an error
                if 'error' in data:
                    error_message = f"API Error: {data['error']['info']}"
                else:
                    # Extracting the needed information from Weatherstack format
                    weather_data = {
                        'city': data['location']['name'],
                        'temperature': data['current']['temperature'],
                        'description': data['current']['weather_descriptions'][0] if data['current']['weather_descriptions'] else "Unknown",
                        'icon': data['current']['weather_icons'][0] if data['current']['weather_icons'] else "",
                        'humidity': data['current']['humidity'],
                        'wind_speed': data['current']['wind_speed'],
                        'country': data['location']['country']
                    }
                
            except requests.exceptions.RequestException:
                error_message = "Error fetching weather data. Please try again."
            except (KeyError, IndexError):
                error_message = "Could not process weather data for this city."
            except Exception as e:
                error_message = f"An unexpected error occurred: {str(e)}"
    
    context = {
        'weather_data': weather_data,
        'error_message': error_message
    }
    
    return render(request, 'weather_app/index.html', context)
