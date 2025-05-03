# utils/voice_handler_web.py

import streamlit as st
import streamlit.components.v1 as components

class VoiceHandlerWeb:
    """Web-compatible voice handler that avoids pyttsx3 issues"""
    
    def __init__(self):
        self.supported = True
    
    def speak(self, text):
        """Display text instead of speaking it"""
        st.info(f"🔊 {text}")
    
    def narrate_route(self, route_data):
        """Display route directions as text"""
        if not route_data:
            st.error("Sorry, I couldn't find a route.")
            return
        
        st.markdown("### 🎤 Voice Navigation (Text Display)")
        
        intro = f"Your journey will be {route_data['distance']} and take approximately {route_data['duration']}."
        st.info(intro)
        
        st.markdown("#### Directions:")
        for i, step in enumerate(route_data['steps'], 1):
            st.write(f"**Step {i}:** {step}")
        
        # Option to use browser's speech synthesis
        st.markdown("---")
        st.markdown("### 🔊 Browser Text-to-Speech")
        
        # Create a button to trigger browser speech
        if st.button("🗣️ Read Directions Aloud"):
            full_text = intro + " Here are your directions: "
            for i, step in enumerate(route_data['steps'], 1):
                full_text += f"Step {i}: {step}. "
            
            # JavaScript to use browser's speech synthesis
            js_code = f"""
            <script>
            function speakText() {{
                if ('speechSynthesis' in window) {{
                    // Cancel any ongoing speech
                    window.speechSynthesis.cancel();
                    
                    var utterance = new SpeechSynthesisUtterance(`{full_text}`);
                    utterance.rate = 0.9;
                    utterance.pitch = 1.0;
                    utterance.volume = 1.0;
                    
                    // Speak the text
                    window.speechSynthesis.speak(utterance);
                }} else {{
                    alert('Text-to-speech not supported in your browser.');
                }}
            }}
            speakText();
            </script>
            """
            components.html(js_code, height=0)