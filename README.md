# Smart Travel Assistant 🌎

A comprehensive travel planning application that combines route planning, natural language processing, voice navigation, and real-time information services to create an intelligent travel companion.

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
- [Contributing](#contributing)
- [License](#license)

## Features

### 🗺️ Core Functionality
- **Route Planning**: Calculate optimal routes between locations with support for multiple transportation modes
- **Multi-Stop Journeys**: Plan complex trips with multiple waypoints
- **Natural Language Processing**: Understand travel queries in plain English using GPT
- **Voice Navigation**: Text-to-speech functionality for hands-free navigation
- **Real-time Weather**: Get current weather conditions for origin and destination
- **Fuel Cost Calculator**: Estimate trip expenses based on vehicle type and current fuel prices
- **Points of Interest**: Discover restaurants, gas stations, hotels, and other POIs along your route
- **Interactive Maps**: Generate visual route maps with Folium
- **Favorites Management**: Save and quickly access frequent locations

### 🎯 Key Features
- Support for car, bike, and walking routes
- Avoid highways, tolls, and ferries options
- Voice-guided turn-by-turn directions
- Weather-aware trip planning
- Fuel consumption and cost estimates
- POI discovery using OpenStreetMap data
- Natural language query processing
- Cross-platform compatibility

## Architecture

The application follows a modular architecture with specialized components:

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│                 │     │                  │     │                 │
│   Main App      │────▶│  Core Services   │────▶│  External APIs  │
│   (main.py)     │     │  (route_planner, │     │  (GraphHopper,  │
│                 │     │   geocoding,     │     │   OpenWeather,  │
│                 │     │   travel_assist) │     │   OpenAI)       │
│                 │     │                  │     │                 │
└─────────────────┘     └──────────────────┘     └─────────────────┘
         │                       │                        
         │                       │                        
         ▼                       ▼                        
┌─────────────────┐     ┌──────────────────┐              
│                 │     │                  │              
│  UI/Voice       │     │  Data Services   │              
│  (colorama,     │     │  (favorites,     │              
│   pyttsx3)      │     │   POI finder)    │              
│                 │     │                  │              
└─────────────────┘     └──────────────────┘              
```

## Prerequisites

### System Requirements
- Python 3.8 or higher
- Linux/Unix system (for text-to-speech support)
- Internet connection for API services

### Required System Packages
For Ubuntu/Debian systems:
```bash
sudo apt update
sudo apt install espeak libespeak1
```

These packages are required for the text-to-speech functionality.

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
```bash
python main.py
```

### Main Menu Options

1. **Plan a Route**: Basic point-to-point navigation
2. **Multi-Stop Journey**: Plan trips with multiple waypoints
3. **Natural Language Planning**: Use conversational queries like "I want to drive from Boston to NYC avoiding highways"
4. **Manage Favorite Locations**: Save frequently used addresses
5. **Voice Navigation**: Get spoken turn-by-turn directions
6. **Trip Calculator**: Estimate fuel costs and travel time
7. **Find Points of Interest**: Discover nearby amenities
8. **Generate Interactive Map**: Create visual route representations
9. **Exit**: Close the application

### Example Commands

#### Natural Language Queries
- "I want to drive from Boston to NYC avoiding highways"
- "Plan a bike route from Central Park to Brooklyn Bridge"
- "Find the fastest route from the airport to downtown without tolls"

#### Voice Commands
The application will speak directions like:
- "Your journey will be 235 miles and take approximately 4 hours 15 minutes"
- "Step 1: Head north on Main Street for 0.5 miles"
- "Step 2: Turn right onto Highway 95"

## Project Structure

```
smart-travel-assistant/
├── main.py                 # Application entry point
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

- **Python 3.8+**: Primary programming language
- **Requests**: HTTP client for API communication
- **OpenAI**: Natural language processing
- **pyttsx3**: Text-to-speech engine
- **Folium**: Interactive map generation
- **Colorama**: Terminal text formatting
- **python-dotenv**: Environment variable management

### External APIs

1. **GraphHopper API**
   - Endpoint: `https://graphhopper.com/api/1/`
   - Used for: Routing, geocoding
   - Rate limits: Varies by plan

2. **OpenWeatherMap API**
   - Endpoint: `http://api.openweathermap.org/data/2.5/`
   - Used for: Current weather data
   - Rate limits: 60 calls/minute (free tier)

3. **OpenAI API**
   - Model: GPT-3.5-turbo
   - Used for: Natural language understanding
   - Rate limits: Based on subscription

4. **OpenStreetMap Overpass API**
   - Endpoint: `http://overpass-api.de/api/interpreter`
   - Used for: POI discovery
   - Rate limits: Fair use policy

### Key Algorithms

1. **Route Optimization**: Uses GraphHopper's routing engine with configurable parameters
2. **Natural Language Processing**: Leverages GPT-3.5 for query understanding with fallback regex parsing
3. **Geocoding**: Converts addresses to coordinates using GraphHopper's geocoding service
4. **Fuel Calculation**: Estimates costs based on distance, vehicle efficiency, and fuel prices

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
- Keep commits atomic and well-described

## Error Handling

The application includes comprehensive error handling for:
- API failures and rate limits
- Invalid user inputs
- Network connectivity issues
- Missing dependencies
- File system operations

## Security Considerations

- API keys are stored in environment variables
- No sensitive data is logged or stored in plain text
- Input validation prevents injection attacks
- External API calls use HTTPS

## Future Enhancements

- Mobile application development
- Real-time traffic integration
- Machine learning for route optimization
- Multi-language support
- Offline mapping capabilities
- Integration with ride-sharing services

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

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