import requests

class POIFinder:
    def __init__(self):
        # Using OpenStreetMap's Overpass API (free)
        self.overpass_url = "http://overpass-api.de/api/interpreter"
    
    def find_pois(self, lat, lng, radius=5000, poi_type='restaurant'):
        """Find points of interest near a location"""
        # Overpass query to find POIs
        query = f"""
        [out:json];
        node(around:{radius},{lat},{lng})["amenity"="{poi_type}"];
        out body;
        """
        
        try:
            response = requests.get(self.overpass_url, params={'data': query})
            if response.status_code == 200:
                data = response.json()
                pois = []
                for element in data.get('elements', []):
                    name = element.get('tags', {}).get('name', 'Unnamed')
                    pois.append({
                        'name': name,
                        'lat': element['lat'],
                        'lon': element['lon'],
                        'type': poi_type
                    })
                return pois[:10]  # Return top 10
        except:
            pass
        
        return []