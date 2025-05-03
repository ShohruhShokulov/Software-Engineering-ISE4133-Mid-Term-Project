import os
import requests
import urllib.parse

class Geocoder:
    def __init__(self):
        self.api_key = os.getenv('GRAPHHOPPER_API_KEY')
        self.geocode_url = "https://graphhopper.com/api/1/geocode?"
    
    def geocode(self, location):
        params = {
            'q': location,
            'limit': 1,
            'key': self.api_key
        }
        
        response = requests.get(self.geocode_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if 'hits' in data and data['hits']:
                hit = data['hits'][0]
                return {
                    'lat': hit['point']['lat'],
                    'lng': hit['point']['lng'],
                    'name': hit.get('name', location),
                    'country': hit.get('country', ''),
                    'state': hit.get('state', '')
                }
        
        return None