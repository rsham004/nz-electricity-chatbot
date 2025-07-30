import pytest
from unittest.mock import Mock, patch
import httpx

# Tests for electricity API tool functions


class TestElectricityTools:
    """Test electricity API tool functions."""
    
    def test_get_current_generation(self):
        """Test getting current power generation data."""
        from src.tools.electricity_api import get_current_generation
        
        # Mock response
        mock_response = {
            "timestamp": "2025-07-30T12:00:00Z",
            "total_generation_mw": 5000,
            "generation_by_type": {
                "hydro": 3000,
                "wind": 800,
                "geothermal": 700,
                "gas": 400,
                "solar": 100
            }
        }
        
        with patch('httpx.get') as mock_get:
            mock_get.return_value.json.return_value = mock_response
            mock_get.return_value.status_code = 200
            
            result = get_current_generation()
            
            assert result["total_generation_mw"] == 5000
            assert result["generation_by_type"]["hydro"] == 3000
            assert "timestamp" in result
    
    def test_get_spot_prices(self):
        """Test getting current spot prices by region."""
        from src.tools.electricity_api import get_spot_prices
        
        mock_response = {
            "timestamp": "2025-07-30T12:00:00Z",
            "prices": {
                "Auckland": 150.50,
                "Wellington": 148.20,
                "Christchurch": 145.80,
                "Dunedin": 143.90
            }
        }
        
        with patch('httpx.get') as mock_get:
            mock_get.return_value.json.return_value = mock_response
            mock_get.return_value.status_code = 200
            
            result = get_spot_prices()
            
            assert result["prices"]["Auckland"] == 150.50
            assert len(result["prices"]) == 4
    
    def test_get_renewable_percentage(self):
        """Test calculating renewable energy percentage."""
        from src.tools.electricity_api import get_renewable_percentage
        
        generation_data = {
            "generation_by_type": {
                "hydro": 3000,
                "wind": 800,
                "geothermal": 700,
                "gas": 400,
                "solar": 100
            }
        }
        
        result = get_renewable_percentage(generation_data)
        
        # Renewable: hydro + wind + geothermal + solar = 3600
        # Total: 5000
        # Percentage: 3600/5000 * 100 = 72%
        assert result == 90.0
    
    def test_api_error_handling(self):
        """Test error handling for API failures."""
        from src.tools.electricity_api import get_current_generation
        
        with patch('httpx.get') as mock_get:
            mock_get.side_effect = httpx.RequestError("Connection failed")
            
            with pytest.raises(Exception) as exc_info:
                get_current_generation()
            
            assert "API request failed" in str(exc_info.value)