from typing import Any, Dict, Optional
import httpx
from mcp.server.fastmcp import FastMCP

USGS_API_BASE = "https://waterservices.usgs.gov/nwis/iv/"

async def get_current_water_data_values(
    sites: str,
    parameter_codes: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    period: Optional[str] = None,
    format: str = "json"
) -> Dict[str, Any]:
    """
    Fetch instantaneous water data from USGS Water Services API
    
    Args:
        sites: Comma-separated site numbers (e.g., "01646500" or "01646500,01647000")
        parameter_codes: Comma-separated parameter codes (e.g., "00060,00065")
        start_date: Start date in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM)
        end_date: End date in ISO format
        period: Period code (e.g., "P7D" for 7 days)
        format: Output format ("json" or "rdb")
    
    Returns:
        Dictionary containing the API response
    """
    params = {
        "sites": sites,
        "format": format
    }
    
    if parameter_codes:
        params["parameterCd"] = parameter_codes
    if start_date:
        params["startDT"] = start_date
    if end_date:
        params["endDT"] = end_date
    if period:
        params["period"] = period
    
    async with httpx.AsyncClient() as client:
        response = await client.get(USGS_API_BASE, params=params)
        response.raise_for_status()
        if format == "json":
            return response.json()
        else:
            return {"data": response.text}

def register_water_data_tools(mcp: FastMCP):
    """Register water data API tools with the MCP server"""
    
    @mcp.tool()
    async def fetch_usgs_data(
        sites: str,
        parameter_codes: str = "",
        start_date: str = "",
        end_date: str = "",
        period: str = ""
    ) -> Dict[str, Any]:
        """Fetch current water data from USGS for specified sites"""
        return await get_current_water_data_values(
            sites=sites,
            parameter_codes=parameter_codes if parameter_codes else None,
            start_date=start_date if start_date else None,
            end_date=end_date if end_date else None,
            period=period if period else None
        )