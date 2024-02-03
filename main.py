from flask import Flask, request, jsonify, json
import requests
import logging
from flask_caching import Cache



app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': 'redis://redis:6379/0'})

# Define the base URLs for microservices
weather_service_index = 0
football_service_index = 0


football_service_instances = [
    "http://football1:8080",
    "http://football2:8080",
    "http://football3:8080"
]
weather_service_instances = [
    "http://weather1:8080",
    "http://weather2:8080",
    "http://weather3:8080"
]
#Weather routes
#1. Get coordinates of a city, call to the weather api to get that - weather/getCoord/{city}"
@app.route('/weather/coordinates/<city>', methods=['GET'])
def get_coordinates(city):
    cached_response = cache.get(f"coordinates_{city}")
    if cached_response:
        logger.info(f"Retrieved coordinates for {city} from cache.")
        return cached_response, "Response fetched from cache"
    else:
        logger.info(f"Coordinates for {city} not found in cache. Fetching from microservice.")
        instance = get_next_weather_service()
        response = requests.get(f"{instance}/weather/getCoord/{city}")
        if response.status_code == 200:
            # Cache the response and return it
            cache.set(f"coordinates_{city}", response.text, timeout=30)
            return response.text
        else:
            # Return the response text and status code if the status code is not 200
            return (response.text, response.status_code)

#2. Get weather per city for the next 5 days - weather/forecast/{city}
@app.route('/weather/forecast/<city>', methods=['GET'])
def get_5dayforecast(city):
    cached_response = cache.get(f"forecast_{city}")
    if cached_response:
        logger.info(f"Retrieved forecast for {city} from cache.")
        return cached_response, "Response fetched from cache"
    else:
        logger.info(f"Forecast for {city} not found in cache. Fetching from microservice.")
        instance = get_next_weather_service()
        response = requests.get(f"{instance}/weather/forecast/{city}")
        if response.status_code == 200:
            # Cache the response and return it
            cache.set(f"forecast_{city}", response.text, timeout=30)
            return response.text, "Response fetched from microservice and cached"
        else:
            # Return the response text and status code if the status code is not 200
            return (response.text, response.status_code)

#3. Get weather per city for right now- weather/{city}
@app.route('/weather/<city>', methods=['GET'])
def get_todayweather(city):
    cached_response = cache.get(f"weather_{city}")
    if cached_response:
        logger.info(f"Retrieved weather for {city} from cache.")
        return cached_response, "Response fetched from cache"
    else:
        logger.info(f"Weather for {city} not found in cache. Fetching from microservice.")
        instance = get_next_weather_service()
        response = requests.get(f"{instance}/weather/{city}")
        if response.status_code == 200:
            # Cache the response and return it
            cache.set(f"weather_{city}", response.text, timeout=30)
            return response.text, "Response fetched from microservice and cached"
        else:
            # Return the response text and status code if the status code is not 200
            return (response.text, response.status_code)

#4. Choose the warmest day without rain in the next 5 days - weather/warmestday/{city}
@app.route('/weather/warmestday/<city>', methods=['GET'])
def get_warmesweather(city):
    cached_response = cache.get(f"warmest_weather_{city}")
    if cached_response:
        logger.info(f"Retrieved warmest weather for {city} from cache.")
        return cached_response, "Response fetched from cache"
    else:
        logger.info(f"Warmest weather for {city} not found in cache. Fetching from microservice.")
        instance = get_next_weather_service()
        response1 = requests.get(f"{instance}/weather/forecast/{city}")
        if response1.status_code == 200 :
            response = requests.get(f"{instance}/weather/warmestday/{city}")
            if response.status_code == 200:
                # Cache the response and return it
                cache.set(f"warmest_weather_{city}", response.text, timeout=30)
                return response.text, "Response fetched from microservice and cached"
            else:
                # Return the response text and status code if the status code is not 200
                return (response.text, response.status_code)

#Football
# 1. Get all the matches in the premier league in the next 5 days
@app.route('/football/getmatches', methods=['GET'])
def get_match():
    cached_response = cache.get("football_matches")
    if cached_response:
        logger.info("Retrieved football matches from cache.")
        return cached_response, "Response fetched from cache"
    else:
        logger.info("Football matches not found in cache. Fetching from microservice.")
        instance = get_next_football_service()
        response = requests.get(f"{instance}/football/getnextmatches")
        if response.status_code == 200:
            # Cache the response and return it
            cache.set("football_matches", response.text, timeout=30)
            return response.text, "Response fetched from microservice and cached"
        else:
            # Return the response text and status code if the status code is not 200
            return (response.text, response.status_code)

# 2. Get all the venues in the city the user is interested in
@app.route('/football/venues/<city>', methods=['GET'])
def get_football_venues(city):
    cached_response = cache.get(f"football_venues_{city}")
    if cached_response:
        logger.info(f"Retrieved football venues for {city} from cache.")
        return cached_response, "Response fetched from cache"
    else:
        logger.info(f"Football venues for {city} not found in cache. Fetching from microservice.")
        instance = get_next_football_service()
        response = requests.get(f"{instance}/football/venues/{city}")
        if response.status_code == 200:
            response_data = response.json()
            cache.set(f"football_venues_{city}", jsonify(response_data), timeout=30)
            return jsonify(response_data), "Response fetched from microservice and cached"
        else:
            return jsonify({"error": f"Failed to fetch football venues for {city}"}), response.status_code

#3. Find a match between 2 teams in the next 5 days
@app.route('/football/getmatch/<home>/<away>', methods=['GET'])
def get_mat(home, away):
    cached_response = cache.get(f"football_match_{home}_{away}")
    if cached_response:
        logger.info(f"Retrieved match data for {home} vs {away} from cache.")
        return cached_response, "Response fetched from cache"
    else:
        instance1 = get_next_football_service()
        response1 = requests.get(f"{instance1}/football/getnextmatches")

        logger.info(f"Match data for {home} vs {away} not found in cache. Fetching from microservice.")
        instance = get_next_football_service()
        if response1.status_code == 200:
            response = requests.get(f"{instance}/football/getmatch/{home}/{away}")
            if response.status_code == 200:
                cache.set(f"football_match_{home}_{away}", response.text, timeout=30)
                return response.text
            else:
                return response.text, response.status_code

#4. Find all matches in the premier league on a certain day
@app.route('/football/getmatches/<day>', methods=['GET'])
def get_m(day):
    cached_response = cache.get(f"football_matches_{day}")
    if cached_response:
        logger.info(f"Retrieved football matches for {day} from cache.")
        return cached_response, "Response fetched from cache"
    else:
        logger.info(f"Football matches for {day} not found in cache. Fetching from microservice.")
        instance = get_next_football_service()
        response = requests.get(f"{instance}/football/getmatches/{day}")
        if response.status_code == 200:
            cache.set(f"football_matches_{day}", response.text, timeout=30)
            return response.text, "Response fetched from microservice and cached"
        else:
            return response.text, response.status_code

#The combining apis
#1. Combines the match that the user is requesting and it suggests to the user wether to go to
#the match or reschedule based on the weather.
@app.route('/football/plan/<home>/<away>', methods=['GET'])
def get_plan(home, away):
    cached_response = cache.get(f"football_plan_{home}_{away}")
    if cached_response:
        logger.info(f"Retrieved plan for {home} vs {away} from cache.")
        return cached_response, "Response fetched from cache"
    else:
        instance1 = get_next_football_service()
        response1 = requests.get(f"{instance1}/football/getnextmatches")
        logger.info(f"Plan for {home} vs {away} not found in cache. Fetching from microservices.")
        football_instance = get_next_football_service()
        weather_instance = get_next_weather_service()
        response = requests.get(f"{football_instance}/football/getmatch/{home}/{away}")
        if response.status_code == 200:
            data = response.json()  # Parse JSON response
            city = data["city"]
            date = data["date"]
            # Make request to weather service
            weather_response = requests.get(f"{weather_instance}/weather/forecast/{city}")
            if weather_response.status_code == 200:
                weather_new_response = requests.get(f"{weather_instance}/weather/choose/{city}/{date}")
                cache.set(f"football_plan_{home}_{away}", weather_new_response.text, timeout=30)
                return weather_new_response.text, 200, "Response fetched from microservices and cached"
            else:
                return weather_response.text, weather_response.status_code
        else:
            return response.text, response.status_code

# 2. Get the warmest day in the next 5 days and suggest matches on that day in that city
# if there are no matches available, get the matches from any city.
@app.route('/plan/warmest/<city>', methods=['GET'])
def get_plan_warmest(city):
    cached_response = cache.get(f"plan_warmest_{city}")
    if cached_response:
        logger.info(f"Retrieved warmest plan for {city} from cache.")
        return cached_response, "Response fetched from cache"
    else:
        logger.info(f"Warmest plan for {city} not found in cache. Fetching from microservices.")
        football_instance = get_next_football_service()
        weather_instance = get_next_weather_service()
        response = requests.get(f"{weather_instance}/weather/warmestday/{city}")
        if response.status_code == 200:
            data = response.json()  # Parse JSON response
            date = data["date"]
            description = data["description"]
            date1 = str(date)
            date2 = date1.split('T')

            football_response = requests.get(f"{football_instance}/football/getmatches/{date2[0]}")
            if football_response.status_code == 200:
                football_data = football_response.json()
                matches_in_city = [match for match in football_data if match.get("city") == city]
                if matches_in_city:
                    response_data = {
                        "date": date2[0],
                        "description": description,
                        "matches_in_city": matches_in_city
                    }
                    cache.set(f"plan_warmest_{city}", jsonify(response_data), timeout=30)
                    return jsonify(response_data), "Response fetched from microservices and cached"
                else:
                    return jsonify({
                        "date": date2[0],
                        "description": description,
                        "matches_in_city": "No matches in the given city",
                        "alternative_matches_in_UK": football_response.json()
                    })
            else:
                return jsonify({
                    "error": "Football service error",
                    "status_code": football_response.status_code
                }), 500
        else:
            return response.text, response.status_code

#3. Plan the matches for a certain date, get the warmest city to go in
@app.route('/plan/<date>', methods=['GET'])
def plan_today(date):
    cached_response = cache.get(f"plan_{date}")
    if cached_response:
        logger.info(f"Retrieved plan for {date} from cache.")
        return cached_response, "Response fetched from cache"
    else:
        logger.info(f"Plan for {date} not found in cache. Fetching from microservices.")
        football_instance = get_next_football_service()
        weather_instance = get_next_weather_service()
        response = requests.get(f"{football_instance}/football/getmatches/{date}")

        if response.status_code == 200:
            matches = response.json()
            warmest_city = None
            max_temperature = float('-inf')

            for match in matches:
                city = match['city']
                weather_response = requests.get(f"{weather_instance}/weather/{city}")

                if weather_response.status_code == 200:
                    weather_data = weather_response.json()
                    for weather_dat in weather_data:
                        temperature = weather_dat["temperature"]
                        if temperature > max_temperature:
                            max_temperature = temperature
                            warmest_city = city

            if warmest_city:
                response_data = {
                    "warmest_city": warmest_city,
                    "match_in_warmest_city": next((match for match in matches if match['city'] == warmest_city), None),
                    "max_temperature" : round(max_temperature - 273, 2),
                }
                cache.set(f"plan_{date}", jsonify(response_data), timeout=30)
                return jsonify(response_data), "Response fetched from microservices and cached"
            else:
                return jsonify({"message": "No matches found or weather data unavailable for any city"}), 404
        else:
            return jsonify({"error": "Failed to fetch football matches", "status_code": response.status_code}), response.status_code

@app.route('/status', methods=['GET'])
def status():
    instance_football = get_next_football_service()
    instance_weather = get_next_weather_service()

    response_football = requests.get(f'{instance_football}/football/status')
    response_weather = requests.get(f'{instance_weather}/weather/status')
    if response_weather.status_code == 200 and response_football.status_code == 200:
        return "Services and Gateway Active"
    else:
        return response_football.status_code, response_weather.status_code, response_weather.text, response_football.text

def get_next_weather_service():
    global weather_service_index

    for _ in range(len(weather_service_instances)):
        service_instance = weather_service_instances[weather_service_index]
        app.logger.info(f"service is {service_instance}")
        weather_service_index = (weather_service_index + 1) % len(weather_service_instances)
        return service_instance

def get_next_football_service():
    global football_service_index
    for _ in range(len(football_service_instances)):
        service_instance = football_service_instances[football_service_index]
        app.logger.info(f"service is {service_instance}")
        football_service_index= (football_service_index + 1) % len(football_service_instances)
        return service_instance

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)