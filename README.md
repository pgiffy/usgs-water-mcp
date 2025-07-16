# USGS Water MCP

[![smithery badge](https://smithery.ai/badge/@pgiffy/usgs-water-mcp)](https://smithery.ai/server/@pgiffy/usgs-water-mcp)

## Overview

This MCP server provides comprehensive access to USGS water data through three APIs:

1. **USGS Water Services API** - Real-time water measurements (stream flow, gage height, temperature, etc.)
2. **Real-Time Flood Impacts API** - Current flooding conditions and reference points
3. **OGC API** - Monitoring location metadata, agency codes, and geological information

The server is modularly designed with separate API handlers unified through a single entry point.

## Project Structure

```
usgs-water-mcp/
├── main.py                  # Unified entry point
├── water_data_api.py        # USGS Water Services API tools
├── flood_impact_api.py      # Real-Time Flood Impacts API tools
├── ogc_api.py              # OGC API tools
├── current_water_levels.py  # Legacy combined file (deprecated)
├── Dockerfile              # Docker configuration
├── pyproject.toml          # Project dependencies
└── README.md               # This file
```

## Service

If you want a clean web interface that utilizes these tools visit https://aqua-node.onrender.com/landing and help me do some testing!

## Sample Output

Here's an example of fetching stream flow data for the Potomac River:

```json
{
  "name": "USGS:01646500:00060:00000",
  "sourceInfo": {
    "siteName": "POTOMAC RIVER NEAR WASHINGTON, DC",
    "siteCode": [
      {
        "value": "01646500",
        "network": "NWIS",
        "agencyCode": "USGS"
      }
    ]
  },
  "variable": {
    "variableCode": [
      {
        "value": "00060",
        "network": "NWIS",
        "vocabulary": "NWIS:UnitValues",
        "variableName": "Streamflow, ft�/s",
        "variableDescription": "Discharge, cubic feet per second"
      }
    ]
  },
  "values": [
    {
      "value": [
        {
          "value": "6420",
          "qualifiers": ["A"],
          "dateTime": "2023-10-01T12:00:00.000"
        }
      ]
    }
  ]
}
```

## Installation

### Installing via pip

```bash
pip install -e .
```

### Manual Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install httpx mcp
   ```

## Connecting with Claude Desktop

1. Edit your Claude Desktop configuration file:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

2. Add the server configuration:
   ```json
   {
     "mcpServers": {
       "usgs-water": {
         "command": "python",
         "args": ["/path/to/usgs-water-mcp/main.py"]
       }
     }
   }
   ```

3. Restart Claude Desktop

## Available Tools

### Water Data Tools

#### fetch_usgs_data

Fetch instantaneous water data from USGS monitoring stations.

**Parameters:**
- `sites` (required): Comma-separated site numbers (e.g., "01646500" or "01646500,01647000")
- `parameter_codes` (optional): Comma-separated parameter codes (e.g., "00060,00065")
- `start_date` (optional): Start date in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM)
- `end_date` (optional): End date in ISO format
- `period` (optional): Period code (e.g., "P7D" for 7 days)

**Common Parameter Codes:**
- `00060`: Discharge (stream flow)
- `00065`: Gage height
- `00010`: Temperature, water
- `00300`: Dissolved oxygen
- `00400`: pH

**Example Usage:**
```
Get current stream flow for the Potomac River near Washington, DC:
sites: "01646500"
parameter_codes: "00060"
```

### Real-Time Flood Impact Tools

#### get_flooding_reference_points

Get currently flooding reference points (updated every 30 minutes).

#### get_reference_points

Get paginated list of reference points.

**Parameters:**
- `page` (optional): Page number (default: 1)
- `limit` (optional): Number of results per page (default: 100)

#### get_reference_point_by_id

Get specific reference point by ID.

**Parameters:**
- `reference_point_id` (required): The reference point ID

#### get_reference_points_by_state

Get reference points for a specific state.

**Parameters:**
- `state_id` (required): State ID (e.g., "CA", "TX")

#### get_reference_point_by_nwis_id

Get reference point by USGS gage ID.

**Parameters:**
- `nwis_id` (required): USGS National Water Information System site ID

#### get_reference_points_by_nws_id

Get reference points by National Weather Service ID.

**Parameters:**
- `nws_id` (required): National Weather Service location ID

#### get_inactive_reference_points

Get inactive reference points.

#### get_states

Get list of states.

#### get_state_by_id

Get specific state information.

**Parameters:**
- `state_id` (required): State ID (e.g., "CA", "TX")

#### get_counties

Get list of counties.

#### get_counties_by_state

Get counties for a specific state.

**Parameters:**
- `state_id` (required): State ID (e.g., "CA", "TX")

#### get_nws_usgs_crosswalk

Get NWS/USGS crosswalk data.

### OGC API Tools

#### get_monitoring_locations

Get monitoring locations with extensive filtering options.

**Parameters:**
- `bbox` (optional): Bounding box as "minx,miny,maxx,maxy"
- `limit` (optional): Maximum number of results (default: 100)
- `offset` (optional): Starting offset for pagination (default: 0)
- `agency_code` (optional): Filter by agency code (e.g., "USGS")
- `state_code` (optional): Filter by state code (e.g., "CA")
- `county_code` (optional): Filter by county code
- `site_type_code` (optional): Filter by site type code
- `monitoring_location_number` (optional): Specific monitoring location number

#### get_monitoring_location_by_id

Get specific monitoring location by ID.

**Parameters:**
- `location_id` (required): The monitoring location ID

#### get_agency_codes

Get agency identification codes.

**Parameters:**
- `limit` (optional): Maximum number of results (default: 100)
- `offset` (optional): Starting offset for pagination (default: 0)

#### get_altitude_datums

Get vertical datum information (recommended: NAVD88).

**Parameters:**
- `limit` (optional): Maximum number of results (default: 100)
- `offset` (optional): Starting offset for pagination (default: 0)

#### get_aquifer_codes

Get aquifer identification information.

**Parameters:**
- `limit` (optional): Maximum number of results (default: 100)
- `offset` (optional): Starting offset for pagination (default: 0)

#### get_aquifer_types

Get aquifer type information (confined vs unconfined).

**Parameters:**
- `limit` (optional): Maximum number of results (default: 100)
- `offset` (optional): Starting offset for pagination (default: 0)

#### get_coordinate_accuracy_codes

Get coordinate accuracy codes for latitude-longitude values.

**Parameters:**
- `limit` (optional): Maximum number of results (default: 100)
- `offset` (optional): Starting offset for pagination (default: 0)

## Troubleshooting

### Common Issues

1. **API Connection Errors**: Ensure you have an active internet connection and the USGS API is accessible
2. **Invalid Site Numbers**: Verify site numbers exist using the USGS Water Data for the Nation website
3. **No Data Available**: Some sites may not have data for the requested time period or parameters
4. **Rate Limiting**: The USGS API has usage limits; avoid making too many requests in quick succession

### Finding Site Numbers

Use the [USGS Water Data for the Nation](https://waterdata.usgs.gov/nwis) website to find monitoring station site numbers in your area of interest.