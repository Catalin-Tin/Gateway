from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Define the base URLs for microservices
weather_service_base_url = "http://localhost:5193"
football_service_base_url = "http://localhost:5131"
#Weather routes
#1. Get coordinates of a city, call to the weather api to get that - weather/getCoord/{city}"
@app.route('/weather/coordinates/<city>', methods=['GET'])
def get_coordinates(city):
    response = requests.get(f"{weather_service_base_url}/weather/getCoord/{city}")
    if response.status_code == 200:
        # Return a custom message if the status code is 200
        return f"Information {response.text} was added into the database successfully", 200
    else:
        # Return the response text and status code if the status code is not 200
        return (response.text, response.status_code)

#2. Get weather per city for the next 5 days - weather/forecast/{city}
@app.route('/weather/forecast/<city>', methods=['GET'])
def get_5dayforecast(city):
    response = requests.get(f"{weather_service_base_url}/weather/forecast/{city}")
    if response.status_code == 200:
        # Return a custom message if the status code is 200
        return response.text, 200
    else:
        # Return the response text and status code if the status code is not 200
        return (response.text, response.status_code)

#3. Get weather per city for right now- weather/{city}
@app.route('/weather/<city>', methods=['GET'])
def get_todayweather(city):
    response = requests.get(f"{weather_service_base_url}/weather/{city}")
    if response.status_code == 200:
        # Return a custom message if the status code is 200
        return response.text, 200
    else:
        # Return the response text and status code if the status code is not 200
        return (response.text, response.status_code)

#4. Choose the warmest day without rain in the next 5 days - weather/warmestday/{city}
@app.route('/weather/warmestday/<city>', methods=['GET'])
def get_warmesweather(city):
    response = requests.get(f"{weather_service_base_url}/weather/warmestday/{city}")
    if response.status_code == 200:
        # Return a custom message if the status code is 200
        return response.text, 200
    else:
        # Return the response text and status code if the status code is not 200
        return (response.text, response.status_code)

#Football
# 1. Get all the matches in the premier league in the next 5 days
@app.route('/football/getmatches', methods=['GET'])
def get_match():
    response = requests.get(f"{football_service_base_url}/football/getnextmatches")
    if response.status_code == 200:
        return response.text
    else:
        # Return the response text and status code if the status code is not 200
        return (response.text, response.status_code)

# 2. Get all the venues in the city the user is interested in
@app.route('/football/venue/<city>', methods=['GET'])
def get_venues(city):
    response = requests.get(f"{football_service_base_url}/football/venues/{city}")
    if response.status_code == 200:
        return response.text
    else:
        # Return the response text and status code if the status code is not 200
        return (response.text, response.status_code)
#3. Find a match between 2 teams in the next 5 days
@app.route('/football/getmatch/<home>/<away>', methods=['GET'])
def get_mat(home, away):
    response = requests.get(f"{football_service_base_url}/football/getmatch/{home}/{away}")
    if response.status_code == 200:
        return response.text
    else:
        # Return the response text and status code if the status code is not 200
        return (response.text, response.status_code)

#4. Find all matches in the premier league on a certain day
@app.route('/football/getmatches/<day>', methods=['GET'])
def get_m(day):
    response = requests.get(f"{football_service_base_url}/football/getmatches/{day}")
    if response.status_code == 200:
        return response.text
    else:
        # Return the response text and status code if the status code is not 200
        return (response.text, response.status_code)

#The combining apis
#1. Combines the match that the user is request and it suggests to the user weather to go to
#the match or reschedule based on the weather.
@app.route('/football/plan/<home>/<away>', methods=['GET'])
def get_plan(home, away):
    response = requests.get(f"{football_service_base_url}/football/getmatch/{home}/{away}")
    if response.status_code == 200:
        data = response.json()  # Parse JSON response
        city = data["city"]
        date = data["date"]
        # Make request to weather service
        weather_response = requests.get(f"{weather_service_base_url}/weather/forecast/{city}")
        if weather_response.status_code == 200:
            weather_new_response = requests.get(f"{weather_service_base_url}/weather/choose/{city}/{date}")
            return weather_new_response.text, 200
        else:
            return weather_response.text, weather_response.status_code
    else:
        # Return the response text and status code if the status code is not 200
        return response.text, response.status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)