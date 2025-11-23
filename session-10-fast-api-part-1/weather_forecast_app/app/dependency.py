# app/dependency.py

from fastapi import Depends
from sqlmodel import Session
from app.database import get_session
from typing import Annotated
import httpx


#  Database Dependency 

# Type alias for database session dependency
# This makes it easier to use in route handlers
# Usage: def my_route(db: DBSession)
# assign DBSession typing annotation: session, value from get_session
# how to use: session: DBSession
DBSession = Annotated[Session, Depends(get_session)]


# Forecast Client 

class ForecastClient:
    """
    Asynchronous weather forecast client
    Integrates with Open-Meteo API to fetch weather data
    Provides methods to get coordinates and weather information
    """
    
    def __init__(self):
        """
        Initialize HTTP client for async requests
        Timeout set to 10 seconds to prevent hanging requests
        """
        self.client = httpx.AsyncClient(timeout=10.0)
    
    async def get_coordinates(self, city: str) -> tuple[float, float]:
        """
        Step 1: Get latitude and longitude from city name
        Uses Open-Meteo Geocoding API
        
        Args:
            city: Name of the city to look up
            
        Returns:
            tuple: (latitude, longitude) as floats
            
        Raises:
            ValueError: If city is not found in the API
        """
        # Open-Meteo Geocoding API endpoint
        url = "https://geocoding-api.open-meteo.com/v1/search"
        
        # Query parameters for the API request
        params = {
            "name": city,       # City name to search
            "count": 1,         # Return only the first result
            "language": "en",   # Results in English
            "format": "json"    # Response format
        }
        
        # Make async GET request to the API
        response = await self.client.get(url, params=params)
        
        # Raise exception if request failed (4xx or 5xx status)
        response.raise_for_status()
        
        # Parse JSON response
        data = response.json()
        
        # Check if city was found
        # API returns empty results array if city not found
        if "results" not in data or not data["results"]:
            raise ValueError("City not found")
        
        # Extract first result
        result = data["results"][0]
        
        # Return latitude and longitude as tuple
        return result["latitude"], result["longitude"]
    
    async def get_weather(self, latitude: float, longitude: float) -> dict:
        """
        Step 2: Get current weather data from coordinates
        Uses Open-Meteo Weather Forecast API
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            dict: Weather data containing temperature, windspeed, weathercode, time
        """
        # Open-Meteo Weather Forecast API endpoint
        url = "https://api.open-meteo.com/v1/forecast"
        
        # Query parameters for weather request
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": "true"  # Request current weather data
        }
        
        # Make async GET request
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        
        # Parse response and extract current weather
        data = response.json()
        return data["current_weather"]
    
    async def get_forecast_for_city(self, city: str) -> dict:
        """
        Complete workflow: Get weather forecast for a city
        Combines both API calls: geocoding and weather
        
        Args:
            city: Name of the city
            
        Returns:
            dict: Weather data for the city
            
        Raises:
            ValueError: If city is not found
        """
        # Step 1: Get coordinates from city name
        latitude, longitude = await self.get_coordinates(city)
        
        # Step 2: Get weather using coordinates
        weather = await self.get_weather(latitude, longitude)
        
        return weather
    
    async def close(self):
        """
        Close the HTTP client
        Should be called when application shuts down
        """
        await self.client.aclose()


# Global singleton instance of ForecastClient
# Using a single instance across all requests improves performance
_forecast_client: ForecastClient | None = None


def get_forecast_client() -> ForecastClient:
    """
    Dependency function to provide ForecastClient instance
    Uses singleton pattern to reuse the same client
    
    Returns:
        ForecastClient: Shared instance of the weather client
    """
    global _forecast_client
    
    # Create instance if it doesn't exist
    if _forecast_client is None:
        _forecast_client = ForecastClient()
    
    return _forecast_client


# Type alias for forecast client dependency
ForecastClientDep = Annotated[ForecastClient, Depends(get_forecast_client)]