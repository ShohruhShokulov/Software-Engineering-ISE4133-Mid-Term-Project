import os
import openai
import json
import re

class TravelAssistant:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
    
    def process_natural_query(self, query):
        """Process natural language travel queries"""
        prompt = f"""
        Extract travel information from this query: "{query}"
        
        Return a JSON with:
        - origin: starting location
        - destination: ending location
        - vehicle: car/bike/foot (default: car)
        - avoid_options: dict with highways/tolls/ferries as boolean
        
        Example: "I want to drive from Boston to NYC avoiding highways"
        Should return: {{"origin": "Boston", "destination": "NYC", "vehicle": "car", "avoid_options": {{"highways": true}}}}
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a travel planning assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            result = response.choices[0].message.content
            return json.loads(result)
        except:
            # Fallback to regex parsing if GPT fails
            return self.fallback_parser(query)
    
    def fallback_parser(self, query):
        """Simple regex-based parser as fallback"""
        # Extract from/to locations
        from_match = re.search(r'from\s+([^to]+)\s+to', query.lower())
        to_match = re.search(r'to\s+([^avoiding|without]+)', query.lower())
        
        if not from_match or not to_match:
            return None
        
        origin = from_match.group(1).strip()
        destination = to_match.group(1).strip()
        
        # Detect vehicle
        vehicle = 'car'
        if 'bike' in query.lower() or 'bicycle' in query.lower():
            vehicle = 'bike'
        elif 'walk' in query.lower() or 'foot' in query.lower():
            vehicle = 'foot'
        
        # Detect avoid options
        avoid_options = {}
        if 'avoiding highways' in query.lower() or 'avoid highways' in query.lower():
            avoid_options['highways'] = True
        if 'avoiding tolls' in query.lower() or 'avoid tolls' in query.lower():
            avoid_options['tolls'] = True
        
        return {
            'origin': origin,
            'destination': destination,
            'vehicle': vehicle,
            'avoid_options': avoid_options
        }
    
    def generate_trip_summary(self, route_data):
        """Generate a friendly trip summary using GPT"""
        prompt = f"""
        Create a friendly travel summary for this route:
        Distance: {route_data['distance']}
        Duration: {route_data['duration']}
        Weather at origin: {route_data['weather_origin']}
        Weather at destination: {route_data['weather_dest']}
        
        Make it conversational and helpful.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a friendly travel guide."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except:
            return f"Your trip will be {route_data['distance']} and take about {route_data['duration']}."