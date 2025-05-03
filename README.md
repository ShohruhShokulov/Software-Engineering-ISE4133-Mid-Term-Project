# Smart Travel Assistant 🌎

An intelligent, AI-powered travel planning system that combines route planning, natural language processing, voice navigation, and real-time information services.

## 🚀 Live Demo

🌐 **Try it now:** [Smart Travel Assistant](https://travelasistant.streamlit.app/)  
🎥 **Demo Video:** 
[Screencast from 2025년 05월 03일 21시 52분 57초.webm](https://github.com/user-attachments/assets/33581c80-67b2-40a4-a9ec-fa198ff82ae1)

## 📖 Documentation

- 📑 [Detailed Project Documentation](docs/README.md)
- 📝 [Mid-term Project Report](docs/Mid-term_report.docx)
- 🎯 [Presentation Slides](docs/presentation.pptx)
- 🎬 [Team Video Demonstrations](https://drive.google.com/drive/folders/1FRznzqwMkxYZPBJg0VmyU0MaRdcZOHRW)

## 🛠️ Quick Start

### Prerequisites

- Python 3.9+
- pip (Python package manager)
- Internet connection for API services

### Installation
1. Install required packages:
```bash
sudo apt update
sudo apt install espeak libespeak1
```
2. Clone the repository:
```bash
git clone https://github.com/ShohruhShokulov/Software-Engineering-ISE4133-Mid-Term-Project.git
cd Software-Engineering-ISE4133-Mid-Term-Project
```

3. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

### Required API Keys

Create accounts and get API keys from:
- 🗺️ [GraphHopper](https://www.graphhopper.com/) - For routing
- 🌤️ [OpenWeather](https://openweathermap.org/api) - For weather data
- 🤖 [OpenAI](https://platform.openai.com/) - For natural language processing

Add to your `.env` file:
```plaintext
GRAPHHOPPER_API_KEY=your_graphhopper_key
OPENWEATHER_API_KEY=your_openweather_key
OPENAI_API_KEY=your_openai_key
```

### Running the Application

Start the Streamlit app:
```bash
streamlit run src/main.py
```

The app will open in your browser at `http://localhost:8501`

## ✨ Key Features

- 🗺️ **Route Planning** - Multi-stop journeys with car, bike, or walking options
- 💬 **Natural Language** - Ask in plain English: "Find a scenic route to the beach avoiding highways"
- 🎤 **Voice Navigation** - Turn-by-turn directions with text display
- 🌤️ **Weather Integration** - Real-time weather for origin and destination
- ⛽ **Fuel Calculator** - Estimate costs based on vehicle type
- 📍 **POI Finder** - Discover restaurants, gas stations, hotels nearby
- ⭐ **Favorites** - Save frequently used locations

## 👥 Team Contributions

| Team Member | Responsibility | Branches |
|------------|---------------|----------|
| **Shohruh Shokulov** | Team Leader, GPT Integration, Main App, docs | `main`, `gpt_api_integration`, `docs`, `map_genrator` |
| **Abdukarimov Humoyun** | Streamlit Interface, Geocoding | `streamlit`, `geocoding` , `fuel_calculator`|
| **Tsogoo Munkhzul** | Route Planner, POI Finder | `route_planner`, `ppt` |
| **Azizbek Sharifov** | Voice Handler, Weather Service | `voice_weather_api` |


## 📁 Project Structure

```
smart-travel-assistant/
├── main.py                 # Streamlit web application
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── docs/                  # Documentation
│   ├── detailed-documentation.md
│   ├── Mid_term.docx
│   └── presentation.pptx
└── utils/                 # Core modules
    ├── route_planner.py   # Route calculation
    ├── travel_assistant.py # Natural language processing
    ├── voice_handler.py   # Text-to-speech
    └── ...               # Other utility modules
```

## 🚀 Deployment

The application is deployed on Streamlit Cloud. For your own deployment:

1. Fork this repository
2. Connect to Streamlit Cloud
3. Add environment variables in Streamlit dashboard
4. Deploy!

## 🔮 Future Enhancements

- Real-time traffic integration
- Multi-language support
- Offline map functionality
- Mobile application
- User authentication system

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Streamlit team for the excellent framework
- GraphHopper for routing services
- OpenAI for natural language capabilities
- Our professor for guidance throughout the project

---

For detailed technical information, architecture diagrams, and comprehensive documentation, please refer to the [detailed documentation](docs/README.md).
