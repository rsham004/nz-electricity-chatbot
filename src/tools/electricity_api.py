"""Electricity API tool functions for fetching NZ electricity data."""
import httpx
from typing import Dict, Any
import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# API endpoints (using public em6 data)
EM6_BASE_URL = "https://api.em6.co.nz/v1"
EMI_BASE_URL = "https://emi.portal.azure-api.net"


def get_current_generation() -> Dict[str, Any]:
    """
    Fetch current power generation data from NZ electricity API.
    
    Returns:
        Dict containing total generation and breakdown by type
    """
    try:
        # Using em6 public API endpoint
        url = f"{EM6_BASE_URL}/generation/current"
        
        logger.info(f"🔌 Making API request to: {url}")
        
        # Make request
        response = httpx.get(url, timeout=10.0)
        
        logger.info(f"📊 API Response - Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            logger.info(f"✅ Successfully fetched generation data: {data}")
            return data
        else:
            logger.warning(f"⚠️  API returned status {response.status_code}, using mock data")
            # Return mock data for development
            mock_data = {
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
            logger.info(f"📝 Using mock data: {mock_data}")
            return mock_data
    except httpx.RequestError as e:
        logger.error(f"❌ API request failed: {str(e)}")
        raise Exception(f"API request failed: {str(e)}")


def get_spot_prices() -> Dict[str, Any]:
    """
    Fetch current spot prices by region.
    
    Returns:
        Dict containing spot prices for different regions
    """
    try:
        url = f"{EM6_BASE_URL}/prices/spot/current"
        
        logger.info(f"💰 Making price API request to: {url}")
        
        response = httpx.get(url, timeout=10.0)
        
        logger.info(f"📊 Price API Response - Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            logger.info(f"✅ Successfully fetched price data: {data}")
            return data
        else:
            logger.warning(f"⚠️  Price API returned status {response.status_code}, using mock data")
            # Return mock data for development
            mock_data = {
                "timestamp": "2025-07-30T12:00:00Z",
                "prices": {
                    "Auckland": 150.50,
                    "Wellington": 148.20,
                    "Christchurch": 145.80,
                    "Dunedin": 143.90
                }
            }
            logger.info(f"📝 Using mock price data: {mock_data}")
            return mock_data
    except httpx.RequestError as e:
        logger.error(f"❌ Price API request failed: {str(e)}")
        raise Exception(f"API request failed: {str(e)}")


def get_renewable_percentage(generation_data: Dict[str, Any]) -> float:
    """
    Calculate renewable energy percentage from generation data.
    
    Args:
        generation_data: Dict containing generation_by_type
        
    Returns:
        Percentage of renewable energy generation
    """
    generation_by_type = generation_data.get("generation_by_type", {})
    
    renewable_sources = ["hydro", "wind", "geothermal", "solar"]
    
    renewable_total = sum(
        generation_by_type.get(source, 0) 
        for source in renewable_sources
    )
    
    total_generation = sum(generation_by_type.values())
    
    if total_generation == 0:
        return 0.0
    
    return round((renewable_total / total_generation) * 100, 1)


def get_carbon_emissions() -> Dict[str, Any]:
    """
    Fetch current carbon emissions data.
    
    Returns:
        Dict containing carbon intensity information
    """
    try:
        url = f"{EM6_BASE_URL}/emissions/current"
        
        response = httpx.get(url, timeout=10.0)
        
        if response.status_code == 200:
            return response.json()
        else:
            # Return mock data for development
            return {
                "timestamp": "2025-07-30T12:00:00Z",
                "carbon_intensity_gco2_kwh": 82,
                "total_emissions_tonnes_per_hour": 410
            }
    except httpx.RequestError as e:
        raise Exception(f"API request failed: {str(e)}")


def get_generation_by_fuel_type() -> Dict[str, Any]:
    """
    Get detailed generation breakdown by fuel type.
    
    Returns:
        Dict with detailed fuel type breakdown
    """
    generation_data = get_current_generation()
    
    if "generation_by_type" in generation_data:
        total = generation_data["total_generation_mw"]
        breakdown = generation_data["generation_by_type"]
        
        # Calculate percentages
        result = {
            "timestamp": generation_data.get("timestamp"),
            "total_generation_mw": total,
            "breakdown": {}
        }
        
        for fuel_type, mw in breakdown.items():
            result["breakdown"][fuel_type] = {
                "mw": mw,
                "percentage": round((mw / total) * 100, 1) if total > 0 else 0
            }
        
        return result
    
    return generation_data