import pyttsx3

class VoiceHandler:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
    
    def speak(self, text):
        """Convert text to speech"""
        self.engine.say(text)
        self.engine.runAndWait()
    
    def narrate_route(self, route_data):
        """Narrate route directions"""
        if not route_data:
            self.speak("Sorry, I couldn't find a route.")
            return
        
        intro = f"Your journey will be {route_data['distance']} and take approximately {route_data['duration']}."
        self.speak(intro)
        
        self.speak("Here are your directions:")
        for i, step in enumerate(route_data['steps'], 1):
            self.speak(f"Step {i}: {step}")