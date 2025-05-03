import os
import sys
from colorama import init, Fore, Style
from dotenv import load_dotenv
from utils.route_planner import RoutePlanner
from utils.travel_assistant import TravelAssistant
from utils.voice_handler import VoiceHandler
from utils.favorites_manager import FavoritesManager
from utils.poi_finder import POIFinder
from utils.map_generator import MapGenerator
from utils.fuel_calculator import FuelCalculator

# Initialize colorama for colored terminal output
init()

# Load environment variables
load_dotenv()

class TravelApp:
    def __init__(self):
        self.route_planner = RoutePlanner()
        self.travel_assistant = TravelAssistant()
        self.voice_handler = VoiceHandler()
        self.favorites_manager = FavoritesManager()
        self.poi_finder = POIFinder()
        self.map_generator = MapGenerator()
        self.fuel_calculator = FuelCalculator()
        
    def display_banner(self):
        print(Fore.CYAN + """
        🌎 ═══════════════════════════════════════════════ 🌎
                    SMART TRAVEL ASSISTANT
        🚗 ═══════════════════════════════════════════════ 🚗
        """ + Style.RESET_ALL)
    
    def display_menu(self):
        print(Fore.YELLOW + "\n📋 MAIN MENU:" + Style.RESET_ALL)
        print("1️⃣  Plan a Route")
        print("2️⃣  Multi-Stop Journey")
        print("3️⃣  Natural Language Planning")
        print("4️⃣  Manage Favorite Locations")
        print("5️⃣  Voice Navigation")
        print("6️⃣  Trip Calculator (Fuel/Time/Weather)")
        print("7️⃣  Find Points of Interest")
        print("8️⃣  Generate Interactive Map")
        print("9️⃣  Exit")
        
    def run(self):
        self.display_banner()
        
        while True:
            self.display_menu()
            choice = input(Fore.GREEN + "\n🎯 Select an option (1-9): " + Style.RESET_ALL)
            
            if choice == '1':
                self.plan_basic_route()
            elif choice == '2':
                self.plan_multi_stop_route()
            elif choice == '3':
                self.natural_language_planning()
            elif choice == '4':
                self.manage_favorites()
            elif choice == '5':
                self.voice_navigation()
            elif choice == '6':
                self.trip_calculator()
            elif choice == '7':
                self.find_pois()
            elif choice == '8':
                self.generate_map()
            elif choice == '9':
                print(Fore.MAGENTA + "\n👋 Thank you for using Smart Travel Assistant! Safe travels! 🚗💨" + Style.RESET_ALL)
                sys.exit(0)
            else:
                print(Fore.RED + "❌ Invalid option. Please try again." + Style.RESET_ALL)
    
    def plan_basic_route(self):
        print(Fore.CYAN + "\n🗺️  ROUTE PLANNING" + Style.RESET_ALL)
        origin = self.get_location_input("origin")
        destination = self.get_location_input("destination")
        
        vehicle = self.get_vehicle_choice()
        avoid_options = self.get_avoid_options()
        
        route = self.route_planner.get_route(origin, destination, vehicle, avoid_options)
        self.display_route_info(route)
        
        if route and input(Fore.YELLOW + "\n🎤 Would you like voice navigation? (y/n): " + Style.RESET_ALL).lower() == 'y':
            self.voice_handler.narrate_route(route)
    
    def plan_multi_stop_route(self):
        print(Fore.CYAN + "\n🚏 MULTI-STOP JOURNEY PLANNER" + Style.RESET_ALL)
        stops = []
        
        origin = self.get_location_input("origin")
        stops.append(origin)
        
        while True:
            add_stop = input(Fore.YELLOW + "➕ Add a waypoint? (y/n): " + Style.RESET_ALL).lower()
            if add_stop != 'y':
                break
            stop = self.get_location_input(f"waypoint {len(stops)}")
            stops.append(stop)
        
        destination = self.get_location_input("destination")
        stops.append(destination)
        
        vehicle = self.get_vehicle_choice()
        route = self.route_planner.get_multi_stop_route(stops, vehicle)
        self.display_route_info(route)
    
    def natural_language_planning(self):
        print(Fore.CYAN + "\n💬 NATURAL LANGUAGE ROUTE PLANNING" + Style.RESET_ALL)
        query = input(Fore.GREEN + "🗣️  Tell me your travel plans: " + Style.RESET_ALL)
        
        route_info = self.travel_assistant.process_natural_query(query)
        if route_info:
            route = self.route_planner.get_route(
                route_info['origin'], 
                route_info['destination'], 
                route_info.get('vehicle', 'car'),
                route_info.get('avoid_options', {})
            )
            self.display_route_info(route)
            
            # Generate and display trip summary
            if route:
                summary = self.travel_assistant.generate_trip_summary(route)
                print(Fore.CYAN + "\n📝 Trip Summary:" + Style.RESET_ALL)
                print(summary)
    
    def voice_navigation(self):
        print(Fore.CYAN + "\n🎤 VOICE NAVIGATION" + Style.RESET_ALL)
        print("This feature will narrate your route directions.")
        
        origin = self.get_location_input("origin")
        destination = self.get_location_input("destination")
        vehicle = self.get_vehicle_choice()
        
        route = self.route_planner.get_route(origin, destination, vehicle)
        
        if route:
            self.display_route_info(route)
            if input(Fore.YELLOW + "\n🔊 Start voice narration? (y/n): " + Style.RESET_ALL).lower() == 'y':
                self.voice_handler.narrate_route(route)
        else:
            print(Fore.RED + "❌ Could not calculate route." + Style.RESET_ALL)
    
    def trip_calculator(self):
        print(Fore.CYAN + "\n🧮 TRIP CALCULATOR" + Style.RESET_ALL)
        
        origin = self.get_location_input("origin")
        destination = self.get_location_input("destination")
        vehicle = self.get_vehicle_choice()
        
        # Get vehicle type for fuel calculation
        print(Fore.YELLOW + "\n🚗 Vehicle type for fuel calculation:" + Style.RESET_ALL)
        print("1. Car (25 mpg)")
        print("2. SUV (20 mpg)")
        print("3. Truck (18 mpg)")
        print("4. Motorcycle (45 mpg)")
        print("5. Electric (no fuel cost)")
        
        vehicle_types = {'1': 'car', '2': 'suv', '3': 'truck', '4': 'motorcycle', '5': 'electric'}
        vehicle_type = vehicle_types.get(input(Fore.GREEN + "Select vehicle type (1-5): " + Style.RESET_ALL), 'car')
        
        # Get custom fuel price
        fuel_price = input(Fore.GREEN + "Enter fuel price per gallon (press Enter for $3.50): " + Style.RESET_ALL)
        if fuel_price:
            try:
                self.fuel_calculator.set_fuel_price(float(fuel_price))
            except ValueError:
                print(Fore.YELLOW + "Invalid price. Using default $3.50" + Style.RESET_ALL)
        
        route = self.route_planner.get_route(origin, destination, vehicle)
        
        if route:
            self.display_route_info(route)
            print(Fore.CYAN + "\n📊 DETAILED TRIP CALCULATIONS:" + Style.RESET_ALL)
            print(f"⛽ Vehicle type: {vehicle_type}")
            print(f"⛽ Fuel efficiency: {self.fuel_calculator.default_mpg.get(vehicle_type, 25)} mpg")
            print(f"⛽ Fuel price: ${self.fuel_calculator.fuel_price_per_gallon:.2f}/gallon")
    
    def find_pois(self):
        print(Fore.CYAN + "\n📍 POINTS OF INTEREST FINDER" + Style.RESET_ALL)
        
        location = self.get_location_input("location to search near")
        
        print(Fore.YELLOW + "\nPOI Categories:" + Style.RESET_ALL)
        print("1. Restaurants 🍽️")
        print("2. Gas stations ⛽")
        print("3. Hotels 🏨")
        print("4. Hospitals 🏥")
        print("5. Banks 🏦")
        print("6. Parking 🅿️")
        
        poi_types = {
            '1': 'restaurant',
            '2': 'fuel',
            '3': 'hotel',
            '4': 'hospital',
            '5': 'bank',
            '6': 'parking'
        }
        
        choice = input(Fore.GREEN + "Select POI type (1-6): " + Style.RESET_ALL)
        poi_type = poi_types.get(choice, 'restaurant')
        
        # Geocode location
        coords = self.route_planner.geocoder.geocode(location)
        if coords:
            pois = self.poi_finder.find_pois(coords['lat'], coords['lng'], poi_type=poi_type)
            
            if pois:
                print(Fore.CYAN + f"\n📍 Found {len(pois)} {poi_type}s near {location}:" + Style.RESET_ALL)
                for i, poi in enumerate(pois, 1):
                    print(f"{i}. {poi['name']}")
            else:
                print(Fore.YELLOW + f"No {poi_type}s found nearby." + Style.RESET_ALL)
        else:
            print(Fore.RED + "❌ Could not geocode location." + Style.RESET_ALL)
    
    def generate_map(self):
        print(Fore.CYAN + "\n🗺️  MAP GENERATOR" + Style.RESET_ALL)
        
        origin = self.get_location_input("origin")
        destination = self.get_location_input("destination")
        
        print(Fore.YELLOW + "\nMap options:" + Style.RESET_ALL)
        print("1. Interactive route map (local HTML file)")
        print("2. Open in Google Maps")
        
        choice = input(Fore.GREEN + "Select option (1-2): " + Style.RESET_ALL)
        
        if choice == '1':
            # Get route and generate interactive map
            coords_origin = self.route_planner.geocoder.geocode(origin)
            coords_dest = self.route_planner.geocoder.geocode(destination)
            
            if coords_origin and coords_dest:
                route_points = [coords_origin, coords_dest]  # Simplified for demo
                filepath = self.map_generator.generate_route_map(route_points)
                print(Fore.GREEN + f"✅ Map generated and opened in browser!" + Style.RESET_ALL)
                print(f"File saved at: {filepath}")
            else:
                print(Fore.RED + "❌ Could not geocode locations." + Style.RESET_ALL)
        
        elif choice == '2':
            self.map_generator.open_google_maps(origin, destination)
            print(Fore.GREEN + "✅ Opened route in Google Maps!" + Style.RESET_ALL)
    
    def manage_favorites(self):
        print(Fore.CYAN + "\n⭐ FAVORITE LOCATIONS MANAGER" + Style.RESET_ALL)
        print("1. View favorites")
        print("2. Add favorite")
        print("3. Remove favorite")
        
        choice = input(Fore.GREEN + "Select option (1-3): " + Style.RESET_ALL)
        
        if choice == '1':
            favorites = self.favorites_manager.list_favorites()
            if favorites:
                print(Fore.CYAN + "\n⭐ Your saved locations:" + Style.RESET_ALL)
                for name, location in favorites.items():
                    print(f"📍 {name}: {location}")
            else:
                print(Fore.YELLOW + "No favorites saved yet." + Style.RESET_ALL)
        
        elif choice == '2':
            name = input(Fore.GREEN + "Enter nickname (e.g., 'home', 'work'): " + Style.RESET_ALL)
            location = input(Fore.GREEN + "Enter full address: " + Style.RESET_ALL)
            self.favorites_manager.add_favorite(name, location)
            print(Fore.GREEN + f"✅ Added '{name}' to favorites!" + Style.RESET_ALL)
        
        elif choice == '3':
            name = input(Fore.GREEN + "Enter nickname to remove: " + Style.RESET_ALL)
            if self.favorites_manager.remove_favorite(name):
                print(Fore.GREEN + f"✅ Removed '{name}' from favorites!" + Style.RESET_ALL)
            else:
                print(Fore.RED + f"❌ '{name}' not found in favorites." + Style.RESET_ALL)
    
    def get_location_input(self, location_type):
        while True:
            location = input(Fore.GREEN + f"📍 Enter {location_type}: " + Style.RESET_ALL)
            
            # Check if it's a favorite
            favorite = self.favorites_manager.get_favorite(location)
            if favorite:
                print(Fore.CYAN + f"✨ Using favorite location: {favorite}" + Style.RESET_ALL)
                return favorite
            
            if location.strip():
                return location
            else:
                print(Fore.RED + "❌ Location cannot be empty." + Style.RESET_ALL)
    
    def get_vehicle_choice(self):
        print(Fore.YELLOW + "\n🚗 Vehicle options:" + Style.RESET_ALL)
        print("1. Car 🚗")
        print("2. Bike 🚲")
        print("3. Foot 🚶")
        
        choices = {'1': 'car', '2': 'bike', '3': 'foot'}
        choice = input(Fore.GREEN + "Select vehicle (1-3): " + Style.RESET_ALL)
        selected = choices.get(choice, 'car')
        print(Fore.CYAN + f"Selected: {selected}" + Style.RESET_ALL)
        return selected
    
    def get_avoid_options(self):
        avoid_options = {}
        print(Fore.YELLOW + "\n🚫 Avoid options:" + Style.RESET_ALL)
        
        if input("Avoid highways? (y/n): ").lower() == 'y':
            avoid_options['highways'] = True
        if input("Avoid tolls? (y/n): ").lower() == 'y':
            avoid_options['tolls'] = True
        if input("Avoid ferries? (y/n): ").lower() == 'y':
            avoid_options['ferries'] = True
        
        return avoid_options
    
    def display_route_info(self, route):
        if not route:
            print(Fore.RED + "❌ Could not calculate route." + Style.RESET_ALL)
            return
        
        print(Fore.CYAN + "\n📋 ROUTE INFORMATION" + Style.RESET_ALL)
        print(f"📏 Distance: {route['distance']}")
        print(f"⏱️  Duration: {route['duration']}")
        print(f"⛽ Estimated fuel cost: {route['fuel_cost']}")
        
        # Display weather if available
        if 'weather_origin' in route:
            print(f"🌤️  Weather at origin: {route['weather_origin']}")
        if 'weather_dest' in route:
            print(f"🌤️  Weather at destination: {route['weather_dest']}")
        
        print(Fore.YELLOW + "\n📍 Directions:" + Style.RESET_ALL)
        for i, step in enumerate(route['steps'], 1):
            print(f"{i}. {step}")

if __name__ == "__main__":
    app = TravelApp()
    app.run()