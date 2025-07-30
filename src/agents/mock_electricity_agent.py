"""Mock Strands Agent for electricity data queries - works without AWS Bedrock."""
import logging
from typing import Dict, Any
from tools.electricity_api import (
    get_current_generation,
    get_spot_prices,
    get_renewable_percentage,
    get_carbon_emissions,
    get_generation_by_fuel_type
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MockElectricityAgent:
    """Mock agent for handling electricity data queries without AWS dependency."""
    
    def __init__(self):
        self.initialized = False
    
    async def initialize(self):
        """Initialize the mock agent."""
        logger.info("🔧 Initializing mock electricity agent...")
        self.initialized = True
        logger.info("✅ Mock agent initialized successfully")
    
    async def query(self, question: str) -> str:
        """Process a user query and return mock response with real data."""
        logger.info(f"🤖 Mock Agent received query: {question}")
        
        if not self.initialized:
            await self.initialize()
        
        try:
            # Get real electricity data
            generation_data = get_current_generation()
            spot_data = get_spot_prices()
            renewable_pct = get_renewable_percentage(generation_data)
            emissions_data = get_carbon_emissions()
            fuel_breakdown = get_generation_by_fuel_type()
            
            # Generate response based on question type
            question_lower = question.lower()
            
            if "generation" in question_lower or "power" in question_lower:
                response = f"""Based on current New Zealand electricity data:

**Total Generation**: {generation_data['total_generation_mw']} MW

**Generation by Source**:
- Hydro: {generation_data['generation_by_type']['hydro']} MW ({fuel_breakdown['breakdown']['hydro']['percentage']}%)
- Wind: {generation_data['generation_by_type']['wind']} MW ({fuel_breakdown['breakdown']['wind']['percentage']}%)
- Geothermal: {generation_data['generation_by_type']['geothermal']} MW ({fuel_breakdown['breakdown']['geothermal']['percentage']}%)
- Gas: {generation_data['generation_by_type']['gas']} MW ({fuel_breakdown['breakdown']['gas']['percentage']}%)
- Solar: {generation_data['generation_by_type']['solar']} MW ({fuel_breakdown['breakdown']['solar']['percentage']}%)

**Renewable Energy**: {renewable_pct}% of total generation

Data timestamp: {generation_data['timestamp']}"""

            elif "price" in question_lower or "spot" in question_lower:
                prices = spot_data['prices']
                response = f"""Current New Zealand electricity spot prices:

**Regional Prices**:
- Auckland: ${prices['Auckland']:.2f}/MWh
- Wellington: ${prices['Wellington']:.2f}/MWh
- Christchurch: ${prices['Christchurch']:.2f}/MWh
- Dunedin: ${prices['Dunedin']:.2f}/MWh

Data timestamp: {spot_data['timestamp']}"""

            elif "renewable" in question_lower:
                response = f"""New Zealand Renewable Energy Status:

**Current Renewable Percentage**: {renewable_pct}%

**Renewable Sources**:
- Hydro: {generation_data['generation_by_type']['hydro']} MW
- Wind: {generation_data['generation_by_type']['wind']} MW  
- Geothermal: {generation_data['generation_by_type']['geothermal']} MW
- Solar: {generation_data['generation_by_type']['solar']} MW

**Non-Renewable**:
- Gas: {generation_data['generation_by_type']['gas']} MW

New Zealand has one of the highest renewable energy percentages globally!"""

            elif "carbon" in question_lower or "emission" in question_lower:
                response = f"""New Zealand Electricity Carbon Emissions:

**Carbon Intensity**: {emissions_data['carbon_intensity_gco2_kwh']} gCO₂/kWh
**Total Emissions**: {emissions_data['total_emissions_tonnes_per_hour']} tonnes/hour

**Context**: With {renewable_pct}% renewable energy, New Zealand has relatively low carbon intensity compared to many countries.

Data timestamp: {emissions_data['timestamp']}"""

            else:
                # General overview response
                response = f"""New Zealand Electricity Overview:

**Generation**: {generation_data['total_generation_mw']} MW total
**Renewable**: {renewable_pct}% of generation
**Carbon Intensity**: {emissions_data['carbon_intensity_gco2_kwh']} gCO₂/kWh

**Current Mix**:
- Hydro: {fuel_breakdown['breakdown']['hydro']['percentage']}%
- Wind: {fuel_breakdown['breakdown']['wind']['percentage']}%  
- Geothermal: {fuel_breakdown['breakdown']['geothermal']['percentage']}%
- Gas: {fuel_breakdown['breakdown']['gas']['percentage']}%
- Solar: {fuel_breakdown['breakdown']['solar']['percentage']}%

**Average Spot Price**: ${sum(spot_data['prices'].values()) / len(spot_data['prices']):.2f}/MWh

Feel free to ask about specific aspects like generation, prices, or renewable energy!"""

            logger.info(f"✅ Mock agent response generated ({len(response)} chars)")
            return response
            
        except Exception as e:
            logger.error(f"❌ Mock agent error: {str(e)}")
            return "I'm sorry, I encountered an error while processing your request. Please try again later."


async def create_mock_electricity_agent() -> MockElectricityAgent:
    """Create and initialize a mock electricity agent."""
    agent = MockElectricityAgent()
    await agent.initialize()
    return agent