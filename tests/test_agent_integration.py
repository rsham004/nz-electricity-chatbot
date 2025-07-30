import pytest
from unittest.mock import Mock, patch
import asyncio

# Tests for Strands Agent integration


class TestAgentIntegration:
    """Test Strands Agent with electricity tools."""
    
    @pytest.mark.asyncio
    async def test_agent_initialization(self):
        """Test agent initialization with tools."""
        from src.agents.electricity_agent import create_electricity_agent
        
        agent = await create_electricity_agent()
        
        assert agent is not None
        assert hasattr(agent, 'tools')
        assert len(agent.tools) >= 3  # At least 3 tools registered
    
    @pytest.mark.asyncio
    async def test_agent_query_current_generation(self):
        """Test agent handling generation query."""
        from src.agents.electricity_agent import create_electricity_agent
        
        agent = await create_electricity_agent()
        
        # Mock the tool response
        mock_generation = {
            "total_generation_mw": 5000,
            "generation_by_type": {
                "hydro": 3000,
                "wind": 800
            }
        }
        
        with patch.object(agent, 'execute_tool', return_value=mock_generation):
            response = await agent.query("What is the current power generation in NZ?")
            
            assert "5000" in response
            assert "MW" in response or "megawatt" in response.lower()
    
    @pytest.mark.asyncio
    async def test_agent_query_spot_prices(self):
        """Test agent handling spot price query."""
        from src.agents.electricity_agent import create_electricity_agent
        
        agent = await create_electricity_agent()
        
        mock_prices = {
            "prices": {
                "Auckland": 150.50,
                "Wellington": 148.20
            }
        }
        
        with patch.object(agent, 'execute_tool', return_value=mock_prices):
            response = await agent.query("What's the spot price in Auckland?")
            
            assert "150.50" in response or "150.5" in response
            assert "Auckland" in response
    
    @pytest.mark.asyncio
    async def test_agent_query_renewable_energy(self):
        """Test agent handling renewable energy query."""
        from src.agents.electricity_agent import create_electricity_agent
        
        agent = await create_electricity_agent()
        
        mock_data = {
            "renewable_percentage": 82.5,
            "breakdown": {
                "hydro": 60,
                "wind": 15,
                "geothermal": 12,
                "solar": 2.5
            }
        }
        
        with patch.object(agent, 'execute_tool', return_value=mock_data):
            response = await agent.query("How much renewable energy is being generated?")
            
            assert "82.5" in response or "82" in response
            assert "%" in response or "percent" in response.lower()
    
    @pytest.mark.asyncio
    async def test_agent_error_handling(self):
        """Test agent handling of errors gracefully."""
        from src.agents.electricity_agent import create_electricity_agent
        
        agent = await create_electricity_agent()
        
        with patch.object(agent, 'execute_tool', side_effect=Exception("API Error")):
            response = await agent.query("What is the current generation?")
            
            assert "error" in response.lower() or "unable" in response.lower()
            assert "try again" in response.lower() or "sorry" in response.lower()