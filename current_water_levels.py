from typing import Any, Dict, List, Optional
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("current_water_levels")

USGS_API_BASE = "https://waterservices.usgs.gov/nwis/iv/"
RTFI_API_BASE = "https://api.waterdata.usgs.gov/rtfi-api"
OGC_API_BASE = "https://api.waterdata.usgs.gov/ogcapi/v0"

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

async def get_rtfi_data(endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Fetch data from USGS Real-Time Flood Impacts API
    
    Args:
        endpoint: API endpoint (e.g., "referencepoints", "referencepoints/flooding")
        params: Optional query parameters
    
    Returns:
        Dictionary containing the API response
    """
    url = f"{RTFI_API_BASE}/{endpoint}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params or {})
        response.raise_for_status()
        return response.json()

async def get_ogc_data(endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Fetch data from USGS OGC API
    
    Args:
        endpoint: API endpoint (e.g., "collections/monitoring-locations/items")
        params: Optional query parameters
    
    Returns:
        Dictionary containing the API response
    """
    url = f"{OGC_API_BASE}/{endpoint}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params or {})
        response.raise_for_status()
        return response.json()

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

@mcp.tool()
async def get_monitoring_locations(
    bbox: str = "",
    limit: int = 100,
    offset: int = 0,
    agency_code: str = "",
    state_code: str = "",
    county_code: str = "",
    site_type_code: str = "",
    monitoring_location_number: str = ""
) -> Dict[str, Any]:
    """
    Get monitoring locations from USGS OGC API
    
    Args:
        bbox: Bounding box as "minx,miny,maxx,maxy"
        limit: Maximum number of results (default: 100)
        offset: Starting offset for pagination (default: 0)
        agency_code: Filter by agency code (e.g., "USGS")
        state_code: Filter by state code (e.g., "CA")
        county_code: Filter by county code
        site_type_code: Filter by site type code
        monitoring_location_number: Specific monitoring location number
    """
    params = {"limit": limit, "offset": offset}
    
    if bbox:
        params["bbox"] = bbox
    if agency_code:
        params["agency_code"] = agency_code
    if state_code:
        params["state_code"] = state_code
    if county_code:
        params["county_code"] = county_code
    if site_type_code:
        params["site_type_code"] = site_type_code
    if monitoring_location_number:
        params["monitoring_location_number"] = monitoring_location_number
    
    return await get_ogc_data("collections/monitoring-locations/items", params)

@mcp.tool()
async def get_monitoring_location_by_id(location_id: str) -> Dict[str, Any]:
    """
    Get specific monitoring location by ID from USGS OGC API
    
    Args:
        location_id: The monitoring location ID
    """
    return await get_ogc_data(f"collections/monitoring-locations/items/{location_id}")

@mcp.tool()
async def get_agency_codes(limit: int = 100, offset: int = 0) -> Dict[str, Any]:
    """
    Get agency identification codes from USGS OGC API
    
    Args:
        limit: Maximum number of results (default: 100)
        offset: Starting offset for pagination (default: 0)
    """
    params = {"limit": limit, "offset": offset}
    return await get_ogc_data("collections/agency-codes/items", params)

@mcp.tool()
async def get_altitude_datums(limit: int = 100, offset: int = 0) -> Dict[str, Any]:
    """
    Get vertical datum information from USGS OGC API
    
    Args:
        limit: Maximum number of results (default: 100)
        offset: Starting offset for pagination (default: 0)
    """
    params = {"limit": limit, "offset": offset}
    return await get_ogc_data("collections/altitude-datums/items", params)

@mcp.tool()
async def get_aquifer_codes(limit: int = 100, offset: int = 0) -> Dict[str, Any]:
    """
    Get aquifer identification information from USGS OGC API
    
    Args:
        limit: Maximum number of results (default: 100)
        offset: Starting offset for pagination (default: 0)
    """
    params = {"limit": limit, "offset": offset}
    return await get_ogc_data("collections/aquifer-codes/items", params)

@mcp.tool()
async def get_aquifer_types(limit: int = 100, offset: int = 0) -> Dict[str, Any]:
    """
    Get aquifer type information from USGS OGC API
    
    Args:
        limit: Maximum number of results (default: 100)
        offset: Starting offset for pagination (default: 0)
    """
    params = {"limit": limit, "offset": offset}
    return await get_ogc_data("collections/aquifer-types/items", params)

@mcp.tool()
async def get_coordinate_accuracy_codes(limit: int = 100, offset: int = 0) -> Dict[str, Any]:
    """
    Get coordinate accuracy codes from USGS OGC API
    
    Args:
        limit: Maximum number of results (default: 100)
        offset: Starting offset for pagination (default: 0)
    """
    params = {"limit": limit, "offset": offset}
    return await get_ogc_data("collections/coordinate-accuracy-codes/items", params)

if __name__ == "__main__":
    mcp.run(transport='stdio')