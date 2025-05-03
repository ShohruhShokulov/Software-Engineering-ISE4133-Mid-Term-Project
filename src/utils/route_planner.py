import os
import requests
import urllib.parse
from .geocoding import Geocoder
from .fuel_calculator import FuelCalculator
from .weather_service import WeatherService

class RoutePlanner:
    def __init__(self):
        self.api_key = os.getenv('GRAPHHOPPER_API_KEY')
        self.route_url = "https://graphhopper.com/api/1/route?"
        self.geocoder = Geocoder()
        self.fuel_calculator = FuelCalculator()
        self.weather_service = WeatherService()
    
    def get_route(self, origin, destination, vehicle='car', avoid_options=None):
        # Geocode locations
        orig_coords = self.geocoder.geocode(origin)
        dest_coords = self.geocoder.geocode(destination)
        
        if not orig_coords or not dest_coords:
            return None
        
        # Build URL
        params = {
            'key': self.api_key,
            'vehicle': vehicle,
            'point': [f"{orig_coords['lat']},{orig_coords['lng']}", 
                     f"{dest_coords['lat']},{dest_coords['lng']}"]
        }
        
        # Add avoid options
        if avoid_options:
            avoid_list = []
            if avoid_options.get('highways'):
                avoid_list.append('motorway')
            if avoid_options.get('tolls'):
                avoid_list.append('toll')
            if avoid_options.get('ferries'):
                avoid_list.append('ferry')
            
            if avoid_list:
                params['avoid'] = ','.join(avoid_list)
        
        # Make request
        response = requests.get(self.route_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            return self.process_route_data(data, orig_coords, dest_coords)
        
        return None
    
    def get_multi_stop_route(self, stops, vehicle='car'):
        if len(stops) < 2:
            return None
        
        # Geocode all stops
        coords = []
        for stop in stops:
            coord = self.geocoder.geocode(stop)
            if coord:
                coords.append(coord)
        
        if len(coords) < 2:
            return None
        
        # Build URL with multiple points
        params = {
            'key': self.api_key,
            'vehicle': vehicle,
            'point': [f"{coord['lat']},{coord['lng']}" for coord in coords]
        }
        
        response = requests.get(self.route_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            return self.process_route_data(data, coords[0], coords[-1])
        
        return None
    
    def process_route_data(self, data, origin, destination):
        if 'paths' not in data or not data['paths']:
            return None
        
        path = data['paths'][0]
        distance_km = path['distance'] / 1000
        distance_miles = distance_km / 1.61
        
        duration_ms = path['time']
        hours = int(duration_ms / 3600000)
        minutes = int((duration_ms % 3600000) / 60000)
        
        # Calculate fuel cost
        fuel_cost = self.fuel_calculator.calculate_cost(distance_miles)
        
        # Get weather
        weather_origin = self.weather_service.get_weather(origin['lat'], origin['lng'])
        weather_dest = self.weather_service.get_weather(destination['lat'], destination['lng'])
        
        # Extract steps
        steps = []
        if 'instructions' in path:
            for instruction in path['instructions']:
                text = instruction.get('text', '')
                distance = instruction.get('distance', 0)
                steps.append(f"{text} ({distance/1000:.1f} km)")
        
        return {
            'distance': f"{distance_miles:.1f} miles / {distance_km:.1f} km",
            'duration': f"{hours}h {minutes}m",
            'fuel_cost': fuel_cost,
            'weather_origin': weather_origin,
            'weather_dest': weather_dest,
            'steps': steps
        }