"""
Travel-related tools for the travel planning application.
This module contains functions for weather data retrieval and flight searches.
"""

import os
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional, Literal
from dotenv import load_dotenv

def get_weather_data(
    location: str,
    forecast_days: Optional[int] = None,
    include_current: bool = True,
    include_forecast: bool = True,
    include_astro: bool = False,
    include_hourly: bool = False,
    include_alerts: bool = False,
) -> str:
    """
    Get a detailed weather report for a location in a readable format.

    Args:
        location (str): The location to get the weather report for.
        forecast_days (Optional[int]): Number of days for the forecast (1-10).
        include_current (bool): Whether to include current conditions in the output.
        include_forecast (bool): Whether to include forecast data in the output.
        include_astro (bool): Whether to include astronomical data in the output.
        include_hourly (bool): Whether to include hourly forecast data in the output.
        include_alerts (bool): Whether to include weather alerts in the output.

    Returns:
        str: Formatted string with the requested weather data.
    """
    load_dotenv()
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        raise ValueError("WEATHER_API_KEY environment variable is not set")

    BASE_URL = "http://api.weatherapi.com/v1"
    endpoint = 'forecast.json'

    params = {
        'key': api_key,
        'q': location,
        'aqi': 'yes',
        'alerts': 'yes',
    }

    if forecast_days is not None:
        if not 1 <= forecast_days <= 10:
            raise ValueError("forecast_days must be between 1 and 10")
        params['forecast_days'] = forecast_days
    elif include_forecast:
        # If include_forecast is True but forecast_days is not set, default to 3 days
        params['forecast_days'] = 3

    try:
        response = requests.get(f"{BASE_URL}/{endpoint}", params=params)
        response.raise_for_status()
        data = response.json()

        if 'error' in data:
            raise ValueError(f"API Error: {data['error']['message']}")
    except requests.RequestException as e:
        raise requests.RequestException(f"Error making request to WeatherAPI: {str(e)}")

    # Format the report in a more readable way
    report = f"# Weather Report for {data['location']['name']}, {data['location']['country']}\n\n"
    
    # Location information
    report += "## Location Information\n"
    report += f"- **Region**: {data['location']['region']}\n"
    report += f"- **Local Time**: {data['location']['localtime']}\n\n"

    if include_current:
        report += "## Current Conditions\n"
        report += f"- **Condition**: {data['current']['condition']['text']}\n"
        report += f"- **Temperature**: {data['current']['temp_c']}°C / {data['current']['temp_f']}°F\n"
        report += f"- **Feels Like**: {data['current']['feelslike_c']}°C / {data['current']['feelslike_f']}°F\n"
        report += f"- **Humidity**: {data['current']['humidity']}%\n"
        report += f"- **Wind**: {data['current']['wind_kph']} kph / {data['current']['wind_mph']} mph, {data['current']['wind_dir']}\n"
        report += f"- **UV Index**: {data['current']['uv']}\n"
        report += f"- **Precipitation**: {data['current']['precip_mm']} mm / {data['current']['precip_in']} in\n\n"

        if include_astro and 'forecast' in data and 'forecastday' in data['forecast'] and data['forecast']['forecastday']:
            report += "## Astronomical Information (Today)\n"
            astro = data['forecast']['forecastday'][0]['astro']
            report += f"- **Sunrise**: {astro['sunrise']}\n"
            report += f"- **Sunset**: {astro['sunset']}\n"
            report += f"- **Moonrise**: {astro['moonrise']}\n"
            report += f"- **Moonset**: {astro['moonset']}\n"
            report += f"- **Moon Phase**: {astro['moon_phase']}\n\n"

    if include_forecast and 'forecast' in data:
        report += "## Forecast\n"
        for day in data['forecast']['forecastday']:
            report += f"### {day['date']}\n"
            report += f"- **Condition**: {day['day']['condition']['text']}\n"
            report += f"- **Temperature**: Max {day['day']['maxtemp_c']}°C / {day['day']['maxtemp_f']}°F, Min {day['day']['mintemp_c']}°C / {day['day']['mintemp_f']}°F\n"
            report += f"- **Chance of Rain**: {day['day']['daily_chance_of_rain']}%\n"
            report += f"- **Precipitation**: {day['day']['totalprecip_mm']} mm / {day['day']['totalprecip_in']} in\n"
            
            if include_astro:
                report += "#### Astronomical Information\n"
                report += f"- **Sunrise**: {day['astro']['sunrise']}\n"
                report += f"- **Sunset**: {day['astro']['sunset']}\n"
                report += f"- **Moon Phase**: {day['astro']['moon_phase']}\n"

            if include_hourly:
                report += "#### Hourly Forecast\n"
                for hour in day['hour']:
                    hour_time = hour['time'].split(' ')[1]
                    report += f"- **{hour_time}**: {hour['temp_c']}°C / {hour['temp_f']}°F, {hour['condition']['text']}, Chance of rain: {hour['chance_of_rain']}%\n"
            
            report += "\n"

    if include_alerts and 'alerts' in data and 'alert' in data['alerts'] and data['alerts']['alert']:
        report += "## Weather Alerts\n"
        for alert in data['alerts']['alert']:
            report += f"- **{alert['headline']}**\n"
            report += f"  - Event: {alert['event']}\n"
            report += f"  - Effective: {alert['effective']}\n"
            report += f"  - Expires: {alert['expires']}\n"
            if 'desc' in alert:
                description = alert['desc'].replace('\n', ' ')[:200]
                report += f"  - Description: {description}...\n"
            report += "\n"

    # Add clothing recommendations based on temperature
    avg_temp = None
    if include_forecast and 'forecast' in data and data['forecast']['forecastday']:
        temps = [day['day']['avgtemp_c'] for day in data['forecast']['forecastday']]
        avg_temp = sum(temps) / len(temps)
    elif include_current:
        avg_temp = data['current']['temp_c']
    
    if avg_temp is not None:
        report += "## Clothing Recommendations\n"
        if avg_temp < 0:
            report += "- Heavy winter coat, thermal layers, gloves, winter hat, and insulated boots\n"
        elif avg_temp < 10:
            report += "- Winter coat, sweater, long-sleeve shirts, scarf, and warm footwear\n"
        elif avg_temp < 15:
            report += "- Light jacket or coat, sweater, and long pants\n"
        elif avg_temp < 20:
            report += "- Light jacket, long-sleeve shirts, and pants\n"
        elif avg_temp < 25:
            report += "- T-shirts, light pants or shorts, and a light jacket for evenings\n"
        elif avg_temp < 30:
            report += "- Light clothing, shorts, and t-shirts\n"
        else:
            report += "- Very light clothing, sun protection (hat, sunglasses), and consider breathable fabrics\n"
        
        # Add rain gear recommendation if there's a chance of rain
        if include_forecast and 'forecast' in data:
            rain_chances = [day['day']['daily_chance_of_rain'] for day in data['forecast']['forecastday']]
            if any(chance > 30 for chance in rain_chances):
                report += "- Don't forget rain gear: umbrella and/or rain jacket\n"

    return report

def search_flights(
    origin: str,
    destination: str,
    departure_date: str,
    return_date: Optional[str] = None,
    adults: int = 1,
    children: int = 0,
    infants: int = 0,
    travel_class: Optional[str] = None,
    non_stop: bool = False,
    currency: str = "USD",
    max_price: Optional[int] = None,
    max_results: int = 10
) -> str:
    """
    Search for flight offers using Amadeus API.

    Args:
        origin (str): Origin airport or city (e.g., "YYZ", "Boston")
        destination (str): Destination airport or city (e.g., "CDG", "Paris")
        departure_date (str): Departure date in YYYY-MM-DD format
        return_date (Optional[str]): Return date in YYYY-MM-DD format for round trips
        adults (int): Number of adult travelers
        children (int): Number of child travelers
        infants (int): Number of infant travelers
        travel_class (Optional[str]): Preferred travel class (ECONOMY, PREMIUM_ECONOMY, BUSINESS, FIRST)
        non_stop (bool): If True, search for non-stop flights only
        currency (str): Currency code for pricing (default: USD)
        max_price (Optional[int]): Maximum price per traveler
        max_results (int): Maximum number of results to return (default: 10)

    Returns:
        str: Formatted flight search results in markdown format
    """
    # Load environment variables
    load_dotenv()

    # Get API credentials from environment variables
    api_key = os.getenv("AMADEUS_API_KEY")
    api_secret = os.getenv("AMADEUS_API_SECRET")

    if not api_key or not api_secret:
        raise ValueError("AMADEUS_API_KEY and AMADEUS_API_SECRET must be set in .env file")

    # Get access token
    token_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    token_data = {
        "grant_type": "client_credentials",
        "client_id": api_key,
        "client_secret": api_secret
    }

    try:
        token_response = requests.post(token_url, data=token_data)
        token_response.raise_for_status()
        access_token = token_response.json()["access_token"]

        # Search for flights
        url = "https://test.api.amadeus.com/v2/shopping/flight-offers"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        params = {
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDate": departure_date,
            "adults": adults,
            "children": children,
            "infants": infants,
            "currencyCode": currency,
            "max": max_results
        }

        if return_date:
            params["returnDate"] = return_date

        if travel_class:
            params["travelClass"] = travel_class

        if non_stop:
            params["nonStop"] = "true"

        if max_price:
            params["maxPrice"] = max_price

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        flight_data = response.json()
        
        # Format results into markdown
        report = f"# Flight Options from {origin} to {destination}\n\n"
        
        if "data" in flight_data and flight_data["data"]:
            for i, offer in enumerate(flight_data["data"][:max_results], 1):
                # Get total price
                total_price = f"{offer['price']['total']} {offer['price']['currency']}"
                
                # Get flight details
                itineraries = offer["itineraries"]
                
                report += f"## Option {i} - {total_price}\n\n"
                
                # Outbound flight
                report += "### Outbound Journey\n"
                outbound = itineraries[0]
                
                for j, segment in enumerate(outbound["segments"], 1):
                    airline = segment["carrierCode"]
                    flight_number = segment["number"]
                    
                    dep_time = segment["departure"]["at"]
                    dep_airport = segment["departure"]["iataCode"]
                    
                    arr_time = segment["arrival"]["at"]
                    arr_airport = segment["arrival"]["iataCode"]
                    
                    duration = segment.get("duration", "")
                    
                    report += f"- **Segment {j}**: {airline} {flight_number}\n"
                    report += f"  - Departure: {dep_time} from {dep_airport}\n"
                    report += f"  - Arrival: {arr_time} at {arr_airport}\n"
                    report += f"  - Duration: {duration}\n"
                
                # Return flight if exists
                if len(itineraries) > 1:
                    report += "\n### Return Journey\n"
                    return_flight = itineraries[1]
                    
                    for j, segment in enumerate(return_flight["segments"], 1):
                        airline = segment["carrierCode"]
                        flight_number = segment["number"]
                        
                        dep_time = segment["departure"]["at"]
                        dep_airport = segment["departure"]["iataCode"]
                        
                        arr_time = segment["arrival"]["at"]
                        arr_airport = segment["arrival"]["iataCode"]
                        
                        duration = segment.get("duration", "")
                        
                        report += f"- **Segment {j}**: {airline} {flight_number}\n"
                        report += f"  - Departure: {dep_time} from {dep_airport}\n"
                        report += f"  - Arrival: {arr_time} at {arr_airport}\n"
                        report += f"  - Duration: {duration}\n"
                
                report += "\n---\n\n"
        else:
            report += "No flight offers found for your search criteria.\n"
        
        return report
        
    except requests.exceptions.RequestException as e:
        error_message = f"# Error Searching Flights\n\nError searching for flight offers: {str(e)}"
        if hasattr(e, 'response') and e.response is not None:
            error_message += f"\n\nResponse status code: {e.response.status_code}"
            error_message += f"\nResponse content: {e.response.text[:500]}..."
        return error_message