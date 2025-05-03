I'll update the README.md to reflect the new Streamlit-based web interface. Here's the updated version:

# Smart Travel Assistant 🌎

A comprehensive web-based travel planning application built with Streamlit that combines route planning, natural language processing, voice navigation guidance, and real-time information services to create an intelligent travel companion.

## Table of Contents
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Technical Details](#technical-details)
- [Web Interface](#web-interface)
- [Contributing](#contributing)
- [License](#license)

## Features

### 🗺️ Core Functionality
- **Route Planning**: Calculate optimal routes between locations with support for multiple transportation modes
- **Multi-Stop Journeys**: Plan complex trips with multiple waypoints through an intuitive web interface
- **Natural Language Processing**: Understand travel queries in plain English using GPT
- **Voice Navigation Guidance**: Text-based turn-by-turn directions (voice synthesis subject to browser support)
- **Real-time Weather**: Get current weather conditions for origin and destination
- **Fuel Cost Calculator**: Estimate trip expenses based on vehicle type and current fuel prices
- **Points of Interest**: Discover restaurants, gas stations, hotels, and other POIs along your route
- **Interactive Maps**: Generate visual route maps with Folium and Streamlit integration
- **Favorites Management**: Save and quickly access frequent locations

### 🎯 Key Features
- Modern web interface built with Streamlit
- Support for car, bike, and walking routes
- Avoid highways, tolls, and ferries options
- Turn-by-turn directions display
- Weather-aware trip planning
- Fuel consumption and cost estimates
- POI discovery using OpenStreetMap data
- Natural language query processing
- Interactive map visualization
- Cross-browser compatibility

## Architecture

The application has been refactored from a CLI-based system to a modern web application using Streamlit:

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Streamlit     │     │                  │     │                 │
│   Web Interface │────▶│  Core Services   │────▶│  External APIs  │
│   (main.py)     │     │  (route_planner, │     │  (GraphHopper,  │
│                 │     │   geocoding,     │     │   OpenWeather,  │
│                 │     │   travel_assist) │     │   OpenAI)       │
└─────────────────┘     └──────────────────┘     └─────────────────┘
         │                       │                        
         │                       │                        
         ▼                       ▼                        
┌─────────────────┐     ┌──────────────────┐              
│   Map Display   │     │                  │              
│   (Folium +     │     │  Data Services   │              
│   Streamlit)    │     │  (favorites,     │              
│                 │     │   POI finder)    │              
└─────────────────┘     └──────────────────┘              
```

## Prerequisites

### System Requirements
- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection for API services

### Required System Packages
For Ubuntu/Debian systems (optional for voice features):
```bash
sudo apt update
sudo apt install espeak libespeak1
```

Note: The web version provides text-based navigation guidance as a fallback if voice synthesis is not supported by the browser.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/smart-travel-assistant.git
cd smart-travel-assistant
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Configuration

### Environment Variables
Create a `.env` file in the project root with your API keys:

```env
GRAPHHOPPER_API_KEY=your_graphhopper_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
OPENAI_API_KEY=your_openai_api_key
```

**Important**: Never commit your `.env` file to version control. The `.gitignore` file is already configured to exclude it.

### API Keys Required

1. **GraphHopper API**: For routing and geocoding services
   - Sign up at [GraphHopper](https://www.graphhopper.com/)
   - Free tier available with limited requests

2. **OpenWeather API**: For weather information
   - Sign up at [OpenWeatherMap](https://openweathermap.org/api)
   - Free tier includes current weather data

3. **OpenAI API**: For natural language processing
   - Sign up at [OpenAI](https://platform.openai.com/)
   - Requires paid subscription for API access

## Usage

### Starting the Application
Run the Streamlit app:
```bash
streamlit run main.py
```

The application will open in your default web browser, typically at `http://localhost:8501`

### Web Interface Navigation

The application features a sidebar with the following sections:

1. **🗺️ Route Planning**: Basic point-to-point navigation with vehicle and avoidance options
2. **🚏 Multi-Stop Journey**: Plan trips with multiple waypoints
3. **💬 Natural Language**: Use conversational queries for route planning
4. **⭐ Favorites**: Manage saved locations for quick access
5. **🎤 Voice Navigation**: Get step-by-step directions (text-based with optional voice)
6. **🧮 Trip Calculator**: Estimate fuel costs and travel time with detailed metrics
7. **📍 Find POIs**: Discover nearby amenities with customizable search radius
8. **🗺️ Interactive Map**: Generate visual route representations with Folium

### Feature Details

#### Route Planning
- Select origin and destination from favorites or enter custom addresses
- Choose between car, bike, or walking
- Toggle options to avoid highways, tolls, or ferries
- View distance, duration, fuel cost, and weather information
- Access turn-by-turn directions

#### Natural Language Planning
- Enter queries like "I want to drive from Boston to NYC avoiding highways"
- Automatic parsing of origin, destination, vehicle type, and preferences
- Intelligent fallback to regex parsing if GPT is unavailable

#### Interactive Map
- Visualize routes with markers for origin and destination
- Interactive Folium maps embedded in the web interface
- Option to generate Google Maps links for external navigation

## Project Structure

```
smart-travel-assistant/
├── main.py                 # Streamlit web application
├── requirements.txt        # Python dependencies
├── .env                   # API keys (not in repository)
├── .gitignore            # Git ignore rules
├── LICENSE               # MIT License
├── README.md             # This documentation
├── data/                 # Data storage directory
│   ├── favorites.json    # Saved favorite locations
│   └── maps/            # Generated map files
├── scripts/             # Utility scripts
└── utils/               # Core application modules
    ├── __init__.py
    ├── route_planner.py      # Route calculation logic
    ├── geocoding.py          # Address to coordinates conversion
    ├── travel_assistant.py   # Natural language processing
    ├── voice_handler.py      # Text-to-speech functionality
    ├── weather_service.py    # Weather data integration
    ├── fuel_calculator.py    # Fuel cost estimation
    ├── poi_finder.py         # Points of interest discovery
    ├── map_generator.py      # Map visualization
    └── favorites_manager.py  # Favorite locations management
```

## Technical Details

### Core Technologies

- **Streamlit**: Web application framework
- **Python 3.8+**: Primary programming language
- **Folium**: Interactive map generation
- **Streamlit-Folium**: Integration for map display
- **Requests**: HTTP client for API communication
- **OpenAI**: Natural language processing
- **python-dotenv**: Environment variable management

### Web Interface Components

- **Session State Management**: Persistent data across page reloads
- **Custom CSS Styling**: Enhanced visual appearance
- **Responsive Layout**: Adapts to different screen sizes
- **Interactive Widgets**: Sliders, checkboxes, selectboxes for user input
- **Tab-based Navigation**: Organized feature sections
- **Real-time Updates**: Dynamic content rendering

### Voice Navigation Adaptation

The web version includes a `SimpleVoiceHandler` class that:
- Displays route directions as formatted text
- Provides step-by-step navigation guidance
- Includes fallback messages for browser compatibility

## Deployment Options

### Local Development
```bash
streamlit run main.py
```

### Production Deployment
1. **Streamlit Cloud**: Deploy directly from GitHub repository
2. **Docker**: Containerize the application for consistent deployment
3. **Cloud Platforms**: Deploy on AWS, Google Cloud, or Azure with appropriate configurations

## Browser Compatibility

The application is tested on:
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

Note: Voice synthesis features may vary by browser support.

## Performance Optimization

- Efficient session state management
- Caching for API responses
- Lazy loading of map components
- Optimized route calculations

## Security Considerations

- API keys stored in environment variables
- Input validation for all user entries
- HTTPS enforcement in production
- No client-side storage of sensitive data

## Future Enhancements

- Real-time traffic integration
- User authentication and personalized routes
- Route sharing functionality
- Mobile-responsive design improvements
- Advanced caching strategies
- Offline map support
- Integration with booking services

## Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure all API keys are correctly set in the `.env` file
2. **Map Display Issues**: Check browser compatibility with Folium
3. **Voice Features**: Verify browser support for text-to-speech
4. **Slow Performance**: Consider implementing caching for frequent routes

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add docstrings to all functions and classes
- Include unit tests for new features
- Update documentation as needed
- Test across multiple browsers
- Ensure responsive design compatibility

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Streamlit team for the excellent web framework
- GraphHopper for routing services
- OpenStreetMap contributors for map data
- OpenAI for natural language processing capabilities
- The Python community for excellent libraries

## Support

For support, please:
1. Check the [Issues](https://github.com/yourusername/smart-travel-assistant/issues) page
2. Create a new issue with detailed information
3. Contact the maintainers

---

Made with ❤️ by the Smart Travel Assistant Team