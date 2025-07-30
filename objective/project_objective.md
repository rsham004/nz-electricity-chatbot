**NO-NEGOTIABLE RULES** DO not use any other technology and when unsure ask questions to clarify. Create minimal code so the user can understand and explain the code to a customer

# New Zealand Electricity Data Chatbot - Project Objective

## Project Overview
Develop a Streamlit-based chatbot application that leverages AI agents to access and analyze New Zealand electricity generation data through APIs. The application will use the Strands Agents framework with Claude Sonnet 4.0 to provide intelligent insights about electricity data based on user queries.

## Key Components

### 1. Architecture
- **Frontend**: Streamlit web application with chat interface
- **AI Framework**: Strands Agents (pip install strand-agents)
- **LLM**: Claude Sonnet 4.0
- **Data Source**: New Zealand electricity generation APIs (em6, EMI, or Transpower)
- **Tool Function Pattern**: Agent-based architecture with callable tool functions

### 2. Core Features

#### User Interface
- Streamlit chat box for user input
- Real-time response display
- Clean, intuitive interface for asking questions about NZ electricity data

#### AI Agent Capabilities
- Natural language understanding of electricity-related queries
- Dynamic tool selection based on user questions
- Data retrieval from electricity APIs
- Intelligent analysis and insights generation

#### Example Queries
- "What is the power currently generated in New Zealand?"
- "Show me the breakdown of generation by fuel type"
- "What's the current spot price in Auckland?"
- "How much renewable energy is being generated right now?"
- "Compare hydro vs wind generation today"

### 3. Technical Implementation

#### Tool Functions
Create Python functions that:
- Connect to em6/EMI APIs for real-time data
- Parse and structure electricity data
- Handle API authentication and rate limiting
- Return formatted data for the agent to analyze

#### Agent Architecture
- Initialize Strands Agent with Claude Sonnet 4.0
- Register tool functions for API access
- Implement function calling pattern for dynamic tool selection
- Process natural language queries and map to appropriate tools

#### Streamlit Integration
- Chat interface component
- Session state management for conversation history
- Async handling for API calls
- Error handling and user feedback

### 4. Data Sources

#### Primary API Options
1. **em6 API**
   - Real-time generation data
   - Spot prices by region
   - Carbon emissions data
   - API Integration Guide: https://www.ems.co.nz/em6-api-integration-guide/

2. **EMI (Electricity Market Information) API**
   - Market statistics
   - Historical data
   - Developer Portal: https://emi.developer.azure-api.net/

### 5. Development Workflow

#### Phase 1: Setup & Authentication
- Install required packages (streamlit, strand-agents)
- Set up API credentials for electricity data sources
- Configure Claude API access

#### Phase 2: Tool Function Development
- Create functions for each data endpoint
- Implement data parsing and formatting
- Add error handling and retry logic

#### Phase 3: Agent Integration
- Initialize Strands Agent with tool functions
- Configure prompt templates for electricity domain
- Test function calling capabilities

#### Phase 4: Streamlit Application
- Build chat interface
- Integrate agent invocation
- Add session management
- Implement response streaming

#### Phase 5: Testing & Refinement
- Test various query types
- Optimize response times
- Improve error messages
- Enhance data visualizations (optional)

### 6. Success Criteria
- Users can ask natural language questions about NZ electricity data
- Agent correctly selects and uses appropriate tools
- Real-time data is accurately retrieved and presented
- Responses include meaningful insights, not just raw data
- Application handles errors gracefully
- Response times are acceptable (< 5 seconds for most queries)

### 7. Future Enhancements
- Data visualization components (charts, graphs)
- Historical data comparisons
- Predictive analytics
- Export functionality for data/reports
- Multiple electricity market support
- Scheduled reports or alerts

## Technical Stack Summary
- **Language**: Python
- **Web Framework**: Streamlit
- **AI Framework**: Strands Agents
- **LLM**: Claude Sonnet 4.0
- **APIs**: em6, EMI, or Transpower electricity data APIs
- **Architecture Pattern**: Tool-calling AI agents