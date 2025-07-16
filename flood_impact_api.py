from typing import Any, Dict, List, Optional, Union
import httpx
from mcp.server.fastmcp import FastMCP

RTFI_API_BASE = "https://api.waterdata.usgs.gov/rtfi-api"

async def get_rtfi_data(endpoint: str, params: Optional[Dict[str, Any]] = None) -> Union[Dict[str, Any], List[Any]]:
    """
    Fetch data from USGS Real-Time Flood Impacts API
    
    Args:
        endpoint: API endpoint (e.g., "referencepoints", "referencepoints/flooding")
        params: Optional query parameters
    
    Returns:
        Dictionary or list containing the API response
    """
    url = f"{RTFI_API_BASE}/{endpoint}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params or {})
        response.raise_for_status()
        data = response.json()
        # Ensure we always return a dict for MCP compatibility
        if isinstance(data, list):
            return {"items": data, "count": len(data)}
        return data

def register_flood_impact_tools(mcp: FastMCP):
    """Register flood impact API tools with the MCP server"""
    
    @mcp.tool()
    async def get_flooding_reference_points() -> Dict[str, Any]:
        """Get currently flooding reference points from USGS Real-Time Flood Impacts API"""
        return await get_rtfi_data("referencepoints/flooding")

    @mcp.tool()
    async def get_reference_points(page: int = 1, limit: int = 100) -> Dict[str, Any]:
        """
        Get paginated list of reference points from USGS Real-Time Flood Impacts API
        
        Args:
            page: Page number (default: 1)
            limit: Number of results per page (default: 100)
        """
        params = {"page": page, "limit": limit}
        return await get_rtfi_data("referencepoints", params)

    @mcp.tool()
    async def get_reference_point_by_id(reference_point_id: str) -> Dict[str, Any]:
        """
        Get specific reference point by ID from USGS Real-Time Flood Impacts API
        
        Args:
            reference_point_id: The reference point ID
        """
        return await get_rtfi_data(f"referencepoints/{reference_point_id}")

    @mcp.tool()
    async def get_reference_points_by_state(state_id: str) -> Dict[str, Any]:
        """
        Get reference points for a specific state from USGS Real-Time Flood Impacts API
        
        Args:
            state_id: State ID (e.g., "CA", "TX")
        """
        return await get_rtfi_data(f"referencepoints/state/{state_id}")

    @mcp.tool()
    async def get_reference_point_by_nwis_id(nwis_id: str) -> Dict[str, Any]:
        """
        Get reference point by USGS gage ID from USGS Real-Time Flood Impacts API
        
        Args:
            nwis_id: USGS National Water Information System site ID
        """
        return await get_rtfi_data(f"referencepoints/nwis/{nwis_id}")

    @mcp.tool()
    async def get_reference_points_by_nws_id(nws_id: str) -> Dict[str, Any]:
        """
        Get reference points by National Weather Service ID from USGS Real-Time Flood Impacts API
        
        Args:
            nws_id: National Weather Service location ID
        """
        return await get_rtfi_data(f"referencepoints/nws/{nws_id}")

    @mcp.tool()
    async def get_inactive_reference_points() -> Dict[str, Any]:
        """Get inactive reference points from USGS Real-Time Flood Impacts API"""
        return await get_rtfi_data("referencepoints/inactive")

    @mcp.tool()
    async def get_states() -> Dict[str, Any]:
        """Get list of states from USGS Real-Time Flood Impacts API"""
        return await get_rtfi_data("states")

    @mcp.tool()
    async def get_state_by_id(state_id: str) -> Dict[str, Any]:
        """
        Get specific state information from USGS Real-Time Flood Impacts API
        
        Args:
            state_id: State ID (e.g., "CA", "TX")
        """
        return await get_rtfi_data(f"states/{state_id}")

    @mcp.tool()
    async def get_counties() -> Dict[str, Any]:
        """Get list of counties from USGS Real-Time Flood Impacts API"""
        return await get_rtfi_data("counties")

    @mcp.tool()
    async def get_counties_by_state(state_id: str) -> Dict[str, Any]:
        """
        Get counties for a specific state from USGS Real-Time Flood Impacts API
        
        Args:
            state_id: State ID (e.g., "CA", "TX")
        """
        return await get_rtfi_data(f"counties/state/{state_id}")

    @mcp.tool()
    async def get_nws_usgs_crosswalk() -> Dict[str, Any]:
        """Get NWS/USGS crosswalk data from USGS Real-Time Flood Impacts API"""
        return await get_rtfi_data("nws_usgs")