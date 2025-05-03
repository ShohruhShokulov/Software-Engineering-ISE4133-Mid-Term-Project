import folium
import webbrowser
import os

class MapGenerator:
    def __init__(self):
        self.output_dir = 'data/maps'
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_route_map(self, route_points, filename='route_map.html'):
        """Generate an interactive map with the route"""
        if not route_points or len(route_points) < 2:
            return None
        
        # Create map centered on first point
        first_point = route_points[0]
        m = folium.Map(location=[first_point['lat'], first_point['lng']], zoom_start=10)
        
        # Add markers for start and end
        folium.Marker(
            [route_points[0]['lat'], route_points[0]['lng']],
            popup='Start',
            icon=folium.Icon(color='green')
        ).add_to(m)
        
        folium.Marker(
            [route_points[-1]['lat'], route_points[-1]['lng']],
            popup='Destination',
            icon=folium.Icon(color='red')
        ).add_to(m)
        
        # Add route line
        coordinates = [[point['lat'], point['lng']] for point in route_points]
        folium.PolyLine(coordinates, weight=3, color='blue', opacity=0.8).add_to(m)
        
        # Save map
        filepath = os.path.join(self.output_dir, filename)
        m.save(filepath)
        
        # Open in browser
        webbrowser.open('file://' + os.path.realpath(filepath))
        
        return filepath
    
    def open_google_maps(self, origin, destination):
        """Open route in Google Maps"""
        url = f"https://www.google.com/maps/dir/{origin}/{destination}"
        webbrowser.open(url)