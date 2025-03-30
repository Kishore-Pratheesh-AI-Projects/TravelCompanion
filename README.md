# AI Travel Planner

An AI-powered travel planning application that helps you research destinations, find events, check weather, and discover flight options for your next trip.

## Features

- **Destination Research**: Detailed information about your chosen destination
- **Event Discovery**: Find events happening during your travel dates
- **Weather Forecasts**: Get weather predictions for your trip
- **Flight Options**: Search for flight alternatives from your location
- **Comprehensive Reports**: Generate detailed travel plans with all the information you need

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Required API keys:
  - OpenAI API key
  - Serper API key (for web search)
  - Weather API key
  - Amadeus API key and secret (for flight search)

### Installation

1. Clone this repository
```bash
git clone https://github.com/yourusername/travel-planner.git
cd travel-planner
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your API keys:
```
OPENAI_API_KEY=your_openai_api_key
SERPER_API_KEY=your_serper_api_key
WEATHER_API_KEY=your_weather_api_key
AMADEUS_API_KEY=your_amadeus_api_key
AMADEUS_API_SECRET=your_amadeus_api_secret
```

### Running the Application

```bash
python app.py
```

The application will launch a Gradio web interface, typically at http://localhost:7860.

## Usage

1. Enter your current location (for flight searches)
2. Specify your desired destination
3. Input your travel dates
4. List your interests and preferences
5. Click "Initialize Agents" (first-time use)
6. Click "Plan My Trip" to generate your travel plan

## Project Structure

```
travel_planner/
├── app.py                # Main application file with Gradio interface
├── config.py             # Configuration and environment variable handling
├── .env                  # Environment variables (not tracked in git)
├── requirements.txt      # Dependencies
├── README.md             # Documentation
├── tools/
│   ├── __init__.py
│   ├── search_tools.py   # Search-related tools (web, Wikipedia)
│   └── travel_tools.py   # Travel-specific tools (weather, flights)
└── agents/
    ├── __init__.py
    ├── agent_factory.py  # Agent creation functions
    └── agent_tasks.py    # Task-specific agent functions
```

## API Key Resources

- OpenAI API: https://platform.openai.com/
- Serper API: https://serper.dev/
- Weather API: https://www.weatherapi.com/
- Amadeus API: https://developers.amadeus.com/

## License

This project is licensed under the MIT License - see the LICENSE file for details.