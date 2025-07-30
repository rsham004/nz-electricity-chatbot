# NZ Electricity Data Chatbot

A Streamlit chatbot that uses Strands Agents and Claude Sonnet 4.0 to answer questions about New Zealand electricity generation data.

## Features
- Natural language queries about NZ electricity data
- Real-time data from electricity APIs
- AI-powered insights using Claude Sonnet 4.0

## Setup
1. Create virtual environment: `python3 -m venv venv`
2. Activate: `source venv/bin/activate`
3. Install: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and add API keys
5. Run: `streamlit run src/app.py`

## Testing
Run tests with: `pytest tests/`