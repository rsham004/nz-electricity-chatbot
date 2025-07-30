# ⚡ NZ Electricity Data Chatbot

A Streamlit-based chatbot application that leverages AI agents to access and analyze New Zealand electricity generation data through APIs. The application uses the Strands Agents framework with Claude Sonnet 4.0 to provide intelligent insights about electricity data based on user queries.

## 🚀 Features

### Core Functionality
- **Natural Language Queries**: Ask questions in plain English about NZ electricity data
- **Real-time Data**: Fetches current electricity generation, pricing, and emissions data
- **AI-Powered Insights**: Uses Claude Sonnet 4.0 to provide meaningful analysis
- **Multiple Data Sources**: Integrates with em6, EMI, and Transpower APIs

### User Interface
- **Interactive Chat Interface**: Clean Streamlit-based chat experience
- **Example Questions**: One-click example queries in the sidebar
- **Loading States**: Visual feedback during API calls
- **Error Handling**: Graceful error messages and recovery

### Data Capabilities
- Current power generation by fuel type (hydro, wind, geothermal, gas, solar)
- Regional electricity spot prices
- Renewable energy percentage calculations
- Carbon emissions and intensity data
- Historical data comparisons

## 🛠️ Technical Stack

- **Language**: Python 3.12+
- **Web Framework**: Streamlit
- **AI Framework**: Strands Agents
- **LLM**: Claude Sonnet 4.0
- **APIs**: em6, EMI, Transpower electricity data APIs
- **Testing**: pytest with async support
- **Architecture**: Tool-calling AI agents with TDD approach

## 📋 Prerequisites

- Python 3.12 or higher
- Claude API key (from Anthropic)
- Git

## 🔧 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/rsham004/nz-electricity-chatbot.git
cd nz-electricity-chatbot
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```env
# Required: Claude API Key
ANTHROPIC_API_KEY=your_claude_api_key_here

# Optional: Electricity API Keys (if required)
EM6_API_KEY=your_em6_api_key_here
EMI_API_KEY=your_emi_api_key_here
```

### 5. Run the Application
```bash
streamlit run src/app.py
```

The application will open in your browser at `http://localhost:8501`

## 🧪 Testing

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test Suites
```bash
# API Tools Tests
pytest tests/test_electricity_tools.py -v

# Agent Integration Tests  
pytest tests/test_agent_integration.py -v

# UI Component Tests
pytest tests/test_streamlit_ui.py -v
```

### Test Coverage
The project includes comprehensive tests for:
- ✅ Electricity API tool functions (4 tests)
- ✅ Strands Agent integration (5 tests)
- ✅ Streamlit UI components (6 tests)
- **Total: 15 tests, all passing**

## 💬 Example Queries

Try asking these questions in the chatbot:

- "What is the current power generation in New Zealand?"
- "Show me the breakdown of generation by fuel type"
- "What's the current spot price in Auckland?"
- "How much renewable energy is being generated right now?"
- "Compare hydro vs wind generation today"
- "What's the carbon intensity right now?"

## 🏗️ Project Structure

```
nz-electricity-chatbot/
├── src/
│   ├── agents/
│   │   └── electricity_agent.py    # Strands Agent with Claude integration
│   ├── tools/
│   │   └── electricity_api.py      # API tool functions
│   ├── ui/
│   │   └── chat_interface.py       # Streamlit UI components
│   └── app.py                      # Main application entry point
├── tests/
│   ├── test_agent_integration.py   # Agent integration tests
│   ├── test_electricity_tools.py   # API tools tests
│   └── test_streamlit_ui.py       # UI component tests
├── objective/
│   └── project_objective.md       # Project requirements and scope
├── requirements.txt               # Python dependencies
├── .env.example                  # Environment variables template
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

## 🔌 API Integration

### Data Sources
1. **em6 API**: Primary source for generation and pricing data
2. **EMI API**: Market statistics and historical data
3. **Transpower**: System operator data

### Available Tools
The agent has access to 5 specialized tools:
- `fetch_current_generation()` - Current power generation data
- `fetch_spot_prices()` - Regional electricity prices
- `calculate_renewable_percentage()` - Renewable energy calculations
- `fetch_carbon_emissions()` - Carbon intensity data
- `fetch_generation_breakdown()` - Detailed fuel type breakdown

## 🚨 Error Handling

The application includes robust error handling:
- API connection failures gracefully handled
- Mock data provided for development/testing
- User-friendly error messages
- Automatic retry logic for transient failures

## 🎯 Development Notes

### Test-Driven Development (TDD)
- Tests written before implementation
- Comprehensive mocking for external dependencies
- Async/await pattern properly tested
- CI/CD ready architecture

### Security
- API keys stored in environment variables
- No secrets committed to repository
- Secure error handling (no sensitive data exposed)

## 📊 GitHub Issues

Track development progress through GitHub issues:
- ✅ Issue #1: Implement Electricity API Tools
- ✅ Issue #2: Implement Strands Agent Integration  
- ✅ Issue #3: Build Streamlit Chat Interface
- ✅ Issue #4: Integration Testing and Documentation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Run tests: `pytest tests/ -v`
4. Commit changes: `git commit -m "Description"`
5. Push to branch: `git push origin feature-name`
6. Submit a Pull Request

## 📝 License

This project is open source. Please ensure compliance with API terms of service when using electricity data APIs.

## 🆘 Troubleshooting

### Common Issues

**"ModuleNotFoundError: No module named 'strands'"**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

**"API request failed" errors**
- Check your `.env` file has correct API keys
- Verify network connectivity
- The app uses mock data for development if APIs are unavailable

**Streamlit not starting**
- Ensure you're in the project directory
- Run `streamlit run src/app.py` (not just `app.py`)
- Check that port 8501 is available

For more issues, check the [GitHub Issues](https://github.com/rsham004/nz-electricity-chatbot/issues) page.