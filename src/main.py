import streamlit as st
import os
import sys
from dotenv import load_dotenv
import pandas as pd
import folium
from streamlit_folium import st_folium

# Import your utility modules
from utils.route_planner import RoutePlanner
from utils.travel_assistant import TravelAssistant
# from utils.voice_handler import VoiceHandler  # Comment this out
from utils.favorites_manager import FavoritesManager
from utils.poi_finder import POIFinder
from utils.map_generator import MapGenerator
from utils.fuel_calculator import FuelCalculator

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="Smart Travel Assistant",
    page_icon="🌎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Create a simple voice handler that works in web environment
class SimpleVoiceHandler:
    def narrate_route(self, route_data):
        """Display route directions as text in Streamlit"""
        if not route_data:
            st.error("No route data available.")
            return
        
        st.markdown("### 🎤 Route Narration")
        
        intro = f"Your journey will be {route_data['distance']} and take approximately {route_data['duration']}."
        st.info(intro)
        
        st.markdown("#### Step-by-step Directions:")
        for i, step in enumerate(route_data['steps'], 1):
            st.write(f"**Step {i}:** {step}")
        
        st.warning("Note: Voice narration is not available in the web version. Please read the directions above.")

# Initialize session state
if 'route_planner' not in st.session_state:
    st.session_state.route_planner = RoutePlanner()
    st.session_state.travel_assistant = TravelAssistant()
    st.session_state.voice_handler = SimpleVoiceHandler()  # Use simple handler
    st.session_state.favorites_manager = FavoritesManager()
    st.session_state.poi_finder = POIFinder()
    st.session_state.map_generator = MapGenerator()
    st.session_state.fuel_calculator = FuelCalculator()

# Custom CSS
st.markdown("""
<style>
    .stAlert {
        padding: 1rem;
        margin: 1rem 0;
    }
    .route-info {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .poi-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        margin: 5px 0;
        border: 1px solid #e0e0e0;
    }
    .step-card {
        background-color: #f8f9fa;
        padding: 10px;
        margin: 5px 0;
        border-left: 4px solid #0366d6;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🌎 Smart Travel Assistant")
st.markdown("### Your intelligent companion for route planning and travel")

# Sidebar navigation
with st.sidebar:
    st.image("https://api.dicebear.com/7.x/shapes/svg?seed=travel", width=150)
    st.title("Navigation")
    
    page = st.radio(
        "Select Function",
        ["🗺️ Route Planning", "🚏 Multi-Stop Journey", "💬 Natural Language", 
         "⭐ Favorites", "🎤 Voice Navigation", "🧮 Trip Calculator", 
         "📍 Find POIs", "🗺️ Interactive Map"],
        key="navigation"
    )

# Main content area
if page == "🗺️ Route Planning":
    st.header("🗺️ Route Planning")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Check for favorites
        favorites = st.session_state.favorites_manager.list_favorites()
        
        origin_options = ["Enter address..."] + list(favorites.keys())
        origin_choice = st.selectbox("Origin", origin_options, key="origin_select")
        
        if origin_choice == "Enter address...":
            origin = st.text_input("Enter origin address", key="origin_input")
        else:
            origin = favorites[origin_choice]
            st.info(f"Using favorite: {origin}")
    
    with col2:
        destination_options = ["Enter address..."] + list(favorites.keys())
        destination_choice = st.selectbox("Destination", destination_options, key="dest_select")
        
        if destination_choice == "Enter address...":
            destination = st.text_input("Enter destination address", key="dest_input")
        else:
            destination = favorites[destination_choice]
            st.info(f"Using favorite: {destination}")
    
    col3, col4 = st.columns(2)
    
    with col3:
        vehicle = st.selectbox(
            "Vehicle",
            ["car", "bike", "foot"],
            format_func=lambda x: {"car": "🚗 Car", "bike": "🚲 Bike", "foot": "🚶 Walking"}[x]
        )
    
    with col4:
        st.write("Avoid Options")
        avoid_highways = st.checkbox("Avoid highways")
        avoid_tolls = st.checkbox("Avoid tolls")
        avoid_ferries = st.checkbox("Avoid ferries")
    
    if st.button("🔍 Calculate Route", type="primary"):
        if origin and destination:
            with st.spinner("Calculating route..."):
                avoid_options = {
                    "highways": avoid_highways,
                    "tolls": avoid_tolls,
                    "ferries": avoid_ferries
                }
                
                route = st.session_state.route_planner.get_route(
                    origin, destination, vehicle, avoid_options
                )
                
                if route:
                    st.success("Route calculated successfully!")
                    
                    # Display route information
                    with st.container():
                        st.markdown("### 📋 Route Information")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Distance", route['distance'])
                        with col2:
                            st.metric("Duration", route['duration'])
                        with col3:
                            st.metric("Fuel Cost", route['fuel_cost'])
                        
                        # Weather information
                        if 'weather_origin' in route and 'weather_dest' in route:
                            col4, col5 = st.columns(2)
                            with col4:
                                st.info(f"🌤️ Origin weather: {route['weather_origin']}")
                            with col5:
                                st.info(f"🌤️ Destination weather: {route['weather_dest']}")
                        
                        # Directions
                        st.markdown("### 📍 Turn-by-turn Directions")
                        for i, step in enumerate(route['steps'], 1):
                            st.markdown(f"**Step {i}:** {step}")
                        
                        # Voice navigation option
                        if st.button("🔊 Start Voice Navigation"):
                            st.session_state.voice_handler.narrate_route(route)
                else:
                    st.error("Could not calculate route. Please check your inputs.")
        else:
            st.warning("Please enter both origin and destination.")

elif page == "🚏 Multi-Stop Journey":
    st.header("🚏 Multi-Stop Journey Planner")
    
    # Initialize stops in session state if not exists
    if 'stops' not in st.session_state:
        st.session_state.stops = []
    
    # Add stops interface
    col1, col2 = st.columns([3, 1])
    with col1:
        new_stop = st.text_input("Add a stop", key="new_stop")
    with col2:
        if st.button("➕ Add Stop"):
            if new_stop:
                st.session_state.stops.append(new_stop)
    
    # Display current stops
    if st.session_state.stops:
        st.write("Current route:")
        for i, stop in enumerate(st.session_state.stops):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"{i+1}. {stop}")
            with col2:
                if st.button("❌", key=f"remove_{i}"):
                    st.session_state.stops.pop(i)
                    st.rerun()
    
    vehicle = st.selectbox("Select vehicle", ["car", "bike", "foot"])
    
    if st.button("🗺️ Calculate Multi-Stop Route"):
        if len(st.session_state.stops) >= 2:
            with st.spinner("Calculating route..."):
                route = st.session_state.route_planner.get_multi_stop_route(
                    st.session_state.stops, vehicle
                )
                
                if route:
                    st.success("Route calculated!")
                    
                    # Display route info
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Distance", route['distance'])
                    with col2:
                        st.metric("Total Duration", route['duration'])
                    with col3:
                        st.metric("Fuel Cost", route['fuel_cost'])
                    
                    # Show directions
                    st.markdown("### Directions")
                    for i, step in enumerate(route['steps'], 1):
                        st.markdown(f"**{i}.** {step}")
                else:
                    st.error("Could not calculate route.")
        else:
            st.warning("Please add at least 2 stops to calculate a route.")

elif page == "💬 Natural Language":
    st.header("💬 Natural Language Route Planning")
    st.write("Describe your travel plans in natural language and I'll help you plan your route.")
    
    query = st.text_area(
        "Tell me about your travel plans:",
        placeholder="e.g., 'I want to drive from Boston to NYC avoiding highways'",
        height=100
    )
    
    if st.button("🚀 Process Query"):
        if query:
            with st.spinner("Understanding your request..."):
                route_info = st.session_state.travel_assistant.process_natural_query(query)
                
                if route_info:
                    st.success("I understood your request!")
                    
                    # Display parsed information
                    st.json(route_info)
                    
                    # Calculate route
                    with st.spinner("Calculating route..."):
                        route = st.session_state.route_planner.get_route(
                            route_info['origin'],
                            route_info['destination'],
                            route_info.get('vehicle', 'car'),
                            route_info.get('avoid_options', {})
                        )
                        
                        if route:
                            # Generate summary
                            summary = st.session_state.travel_assistant.generate_trip_summary(route)
                            st.markdown("### 📝 Trip Summary")
                            st.write(summary)
                            
                            # Display route details
                            st.markdown("### 📋 Route Details")
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Distance", route['distance'])
                            with col2:
                                st.metric("Duration", route['duration'])
                            with col3:
                                st.metric("Fuel Cost", route['fuel_cost'])
                        else:
                            st.error("Could not calculate route.")
                else:
                    st.error("Could not understand your request. Please try rephrasing.")
        else:
            st.warning("Please describe your travel plans.")

elif page == "⭐ Favorites":
    st.header("⭐ Favorite Locations Manager")
    
    tab1, tab2 = st.tabs(["View Favorites", "Add/Remove Favorites"])
    
    with tab1:
        favorites = st.session_state.favorites_manager.list_favorites()
        if favorites:
            st.write("Your saved locations:")
            for name, location in favorites.items():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"📍 **{name}**: {location}")
                with col2:
                    if st.button("Remove", key=f"remove_fav_{name}"):
                        st.session_state.favorites_manager.remove_favorite(name)
                        st.success(f"Removed {name}")
                        st.rerun()
        else:
            st.info("No favorites saved yet.")
    
    with tab2:
        st.subheader("Add New Favorite")
        new_name = st.text_input("Nickname (e.g., 'home', 'work')")
        new_location = st.text_input("Full address")
        
        if st.button("Add Favorite"):
            if new_name and new_location:
                st.session_state.favorites_manager.add_favorite(new_name, new_location)
                st.success(f"Added '{new_name}' to favorites!")
                st.rerun()
            else:
                st.warning("Please fill in both fields.")

elif page == "🎤 Voice Navigation":
    st.header("🎤 Voice Navigation")
    st.info("Note: Voice synthesis may not work in all browsers. Text directions will be displayed as a fallback.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        origin = st.text_input("Origin")
    with col2:
        destination = st.text_input("Destination")
    
    vehicle = st.selectbox("Vehicle", ["car", "bike", "foot"])
    
    if st.button("🎯 Get Directions"):
        if origin and destination:
            with st.spinner("Calculating route..."):
                route = st.session_state.route_planner.get_route(origin, destination, vehicle)
                
                if route:
                    st.success("Route calculated!")
                    
                    # Display route info
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Distance", route['distance'])
                    with col2:
                        st.metric("Duration", route['duration'])
                    
                    # Voice navigation button
                    if st.button("🔊 Start Voice Navigation", type="primary"):
                        st.session_state.voice_handler.narrate_route(route)
                else:
                    st.error("Could not calculate route.")
        else:
            st.warning("Please enter both origin and destination.")

elif page == "🧮 Trip Calculator":
    st.header("🧮 Trip Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        origin = st.text_input("Origin", key="calc_origin")
        vehicle = st.selectbox("Vehicle", ["car", "bike", "foot"], key="calc_vehicle")
    
    with col2:
        destination = st.text_input("Destination", key="calc_dest")
        vehicle_type = st.selectbox(
            "Vehicle Type (for fuel calculation)",
            ["car", "suv", "truck", "motorcycle", "electric"],
            key="vehicle_type"
        )
    
    # Fuel price settings
    with st.expander("⛽ Fuel Settings"):
        fuel_price = st.number_input(
            "Fuel price per gallon ($)",
            value=3.50,
            min_value=0.0,
            step=0.10
        )
        st.session_state.fuel_calculator.set_fuel_price(fuel_price)
        
        mpg_values = {
            'car': 25,
            'suv': 20,
            'truck': 18,
            'motorcycle': 45,
            'electric': 0
        }
        st.write(f"Vehicle efficiency: {mpg_values[vehicle_type]} mpg")
    
    if st.button("Calculate Trip Details"):
        if origin and destination:
            with st.spinner("Calculating..."):
                route = st.session_state.route_planner.get_route(origin, destination, vehicle)
                
                if route:
                    st.success("Calculation complete!")
                    
                    # Display detailed calculations
                    st.markdown("### 📊 Trip Details")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Distance", route['distance'])
                    with col2:
                        st.metric("Duration", route['duration'])
                    with col3:
                        st.metric("Fuel Cost", route['fuel_cost'])
                    
                    # Additional details
                    st.markdown("### Additional Information")
                    st.write(f"⛽ Vehicle type: {vehicle_type}")
                    st.write(f"⛽ Fuel efficiency: {mpg_values[vehicle_type]} mpg")
                    st.write(f"⛽ Fuel price: ${fuel_price:.2f}/gallon")
                    
                    # Weather info
                    if 'weather_origin' in route and 'weather_dest' in route:
                        st.markdown("### 🌤️ Weather")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.info(f"Origin: {route['weather_origin']}")
                        with col2:
                            st.info(f"Destination: {route['weather_dest']}")
                else:
                    st.error("Could not calculate route.")
        else:
            st.warning("Please enter both origin and destination.")

elif page == "📍 Find POIs":
    st.header("📍 Points of Interest Finder")
    
    location = st.text_input("Location to search near")
    
    poi_types = {
        "🍽️ Restaurants": "restaurant",
        "⛽ Gas stations": "fuel",
        "🏨 Hotels": "hotel",
        "🏥 Hospitals": "hospital",
        "🏦 Banks": "bank",
        "🅿️ Parking": "parking"
    }
    
    selected_type = st.selectbox(
        "Type of POI",
        list(poi_types.keys())
    )
    
    radius = st.slider("Search radius (meters)", 1000, 10000, 5000, 500)
    
    if st.button("🔍 Search POIs"):
        if location:
            with st.spinner("Searching..."):
                coords = st.session_state.route_planner.geocoder.geocode(location)
                
                if coords:
                    pois = st.session_state.poi_finder.find_pois(
                        coords['lat'], 
                        coords['lng'], 
                        radius=radius,
                        poi_type=poi_types[selected_type]
                    )
                    
                    if pois:
                        st.success(f"Found {len(pois)} places")
                        
                        # Display POIs
                        for i, poi in enumerate(pois, 1):
                            with st.container():
                                st.markdown(f"### {i}. {poi['name']}")
                                st.write(f"Location: {poi['lat']}, {poi['lon']}")
                                st.write(f"Type: {poi['type']}")
                                st.markdown("---")
                    else:
                        st.info("No places found in this area.")
                else:
                    st.error("Could not geocode location.")
        else:
            st.warning("Please enter a location.")

elif page == "🗺️ Interactive Map":
    st.header("🗺️ Interactive Map Generator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        origin = st.text_input("Origin", key="map_origin")
    with col2:
        destination = st.text_input("Destination", key="map_dest")
    
    map_type = st.radio(
        "Map Type",
        ["Interactive Route Map", "Google Maps Link"]
    )
    
    if st.button("Generate Map"):
        if origin and destination:
            if map_type == "Interactive Route Map":
                with st.spinner("Generating map..."):
                    coords_origin = st.session_state.route_planner.geocoder.geocode(origin)
                    coords_dest = st.session_state.route_planner.geocoder.geocode(destination)
                    
                    if coords_origin and coords_dest:
                        # Create folium map
                        m = folium.Map(
                            location=[coords_origin['lat'], coords_origin['lng']], 
                            zoom_start=10
                        )
                        
                        # Add markers
                        folium.Marker(
                            [coords_origin['lat'], coords_origin['lng']],
                            popup="Start",
                            icon=folium.Icon(color='green')
                        ).add_to(m)
                        
                        folium.Marker(
                            [coords_dest['lat'], coords_dest['lng']],
                            popup="Destination",
                            icon=folium.Icon(color='red')
                        ).add_to(m)
                        
                        # Add line
                        folium.PolyLine(
                            [[coords_origin['lat'], coords_origin['lng']], 
                             [coords_dest['lat'], coords_dest['lng']]],
                            weight=3,
                            color='blue',
                            opacity=0.8
                        ).add_to(m)
                        
                        # Display map
                        st_folium(m, width=700, height=500)
                    else:
                        st.error("Could not geocode locations.")
            else:
                # Generate Google Maps link
                google_maps_url = f"https://www.google.com/maps/dir/{origin}/{destination}"
                st.markdown(f"[Open in Google Maps]({google_maps_url})")
                st.info("Click the link above to view the route in Google Maps.")
        else:
            st.warning("Please enter both origin and destination.")

# Footer
st.markdown("---")
st.markdown("### 🌎 Smart Travel Assistant")
st.markdown("Made with ❤️ for travelers")