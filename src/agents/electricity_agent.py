"""Strands Agent for electricity data queries."""
import os
import logging
from typing import Dict, Any
from strands import Agent, tool

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
from tools.electricity_api import (
    get_current_generation,
    get_spot_prices,
    get_renewable_percentage,
    get_carbon_emissions,
    get_generation_by_fuel_type
)


# Define tools using strands decorator
@tool
def fetch_current_generation() -> Dict[str, Any]:
    """Get current power generation in New Zealand."""
    return get_current_generation()


@tool
def fetch_spot_prices() -> Dict[str, Any]:
    """Get current electricity spot prices by region."""
    return get_spot_prices()


@tool  
def calculate_renewable_percentage() -> float:
    """Calculate current renewable energy percentage."""
    generation_data = get_current_generation()
    return get_renewable_percentage(generation_data)


@tool
def fetch_carbon_emissions() -> Dict[str, Any]:
    """Get current carbon emissions data."""
    return get_carbon_emissions()


@tool
def fetch_generation_breakdown() -> Dict[str, Any]:
    """Get detailed generation breakdown by fuel type with percentages."""
    return get_generation_by_fuel_type()


class ElectricityAgent:
    """Agent for handling electricity data queries."""
    
    def __init__(self):
        self.agent = None
        self.tools = [
            fetch_current_generation,
            fetch_spot_prices,
            calculate_renewable_percentage,
            fetch_carbon_emissions,
            fetch_generation_breakdown
        ]
    
    async def initialize(self):
        """Initialize the agent with tools."""
        self.agent = Agent(
            model="claude-3-5-sonnet-20241022",
            tools=self.tools,
            system_prompt="""You are an expert on New Zealand electricity data. 
            Help users understand electricity generation, pricing, and emissions data.
            Provide clear, concise answers with relevant numbers and insights.
            When asked about current data, use the available tools to fetch real-time information.
            Format monetary values with $ and include units (MW for power, $/MWh for prices)."""
        )
    
    async def execute_tool(self, tool_name: str, **kwargs) -> Any:
        """Execute a specific tool by name (for testing)."""
        tool_map = {
            "get_current_generation": fetch_current_generation,
            "get_spot_prices": fetch_spot_prices,
            "calculate_renewable_percentage": calculate_renewable_percentage,
            "get_carbon_emissions": fetch_carbon_emissions,
            "get_generation_breakdown": fetch_generation_breakdown
        }
        
        if tool_name in tool_map:
            return tool_map[tool_name]()
        raise ValueError(f"Tool {tool_name} not found")
    
    async def query(self, question: str) -> str:
        """Process a user query and return response."""
        logger.info(f"🤖 Agent received query: {question}")
        
        if not self.agent:
            logger.info("🔧 Initializing agent...")
            await self.initialize()
        
        try:
            logger.info("📤 Sending query to agent...")
            response = await self.agent.invoke_async(question)
            result = response.content if hasattr(response, 'content') else str(response)
            logger.info(f"✅ Agent response: {result}")
            return result
        except Exception as e:
            logger.error(f"❌ Agent error: {str(e)}")
            import traceback
            logger.error(f"📋 Full traceback: {traceback.format_exc()}")
            return f"I'm sorry, I encountered an error while processing your request. Please try again later."


async def create_electricity_agent() -> ElectricityAgent:
    """Create and initialize an electricity agent."""
    agent = ElectricityAgent()
    await agent.initialize()
    return agent