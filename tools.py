# tools.py - Modern version
import requests
from typing import Dict
from langchain.tools import tool

@tool
def get_current_location() -> Dict[str, any]:
    """Get the user's current location based on their IP address."""
    try:
        # Using ip-api.com - more generous free tier
        response = requests.get('http://ip-api.com/json/')
        
        # Check if request was successful
        if response.status_code != 200:
            return {
                "city": "Unknown",
                "country": "Unknown", 
                "lat": 0,
                "lon": 0,
                "error": f"API returned status {response.status_code}"
            }
            
        data = response.json()
        
        # Check if the API call was successful
        if data.get('status') == 'success':
            return {
                "city": data.get('city', 'Unknown'),
                "country": data.get('country', 'Unknown'),
                "lat": data.get('lat', 0),
                "lon": data.get('lon', 0)
            }
        else:
            # API returned a failure status
            return {
                "city": "Unknown",
                "country": "Unknown",
                "lat": 0,
                "lon": 0,
                "error": data.get('message', 'Location detection failed')
            }
            
    except Exception as e:
        return {
            "city": "Unknown",
            "country": "Unknown",
            "lat": 0,
            "lon": 0,
            "error": str(e)
        }

@tool
def get_exchange_rate(from_currency: str = "USD", to_currency: str = "INR") -> Dict[str, any]:
    """Get current exchange rate between two currencies.
    
    Args:
        from_currency: Source currency code (default: USD)
        to_currency: Target currency code (default: INR)
    """
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        response = requests.get(url)
        data = response.json()
        
        rate = data['rates'].get(to_currency, None)
        if rate:
            return {
                "from": from_currency,
                "to": to_currency,
                "rate": rate,
                "timestamp": data.get('date', 'Unknown')
            }
        else:
            return {"error": f"Currency {to_currency} not found"}
    except Exception as e:
        return {"error": str(e)}

@tool
def get_weather(location: str) -> Dict[str, any]:
    """Get current weather for a specific city.
    
    Args:
        location: City name (e.g., 'Mumbai', 'London', 'New York')
    """
    try:
        url = f"https://wttr.in/{location}?format=j1"
        response = requests.get(url)
        data = response.json()
        
        current = data['current_condition'][0]
        return {
            "location": location,
            "temperature_c": int(current['temp_C']),
            "temperature_f": int(current['temp_F']),
            "description": current['weatherDesc'][0]['value'],
            "humidity": int(current['humidity']),
            "feels_like_c": int(current['FeelsLikeC'])
        }
    except Exception as e:
        return {"error": str(e)}

# List of all tools
tools = [get_current_location, get_exchange_rate, get_weather]