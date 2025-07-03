# USGS Water MCP

[![smithery badge](https://smithery.ai/badge/@pgiffy/usgs-water-mcp)](https://smithery.ai/server/@pgiffy/usgs-water-mcp)

## Overview

This MCP server provides access to real-time water data from the USGS Water Services API. It allows you to fetch instantaneous water measurements including stream flow, gage height, temperature, and other water quality parameters from thousands of monitoring stations across the United States.

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

### Installing via Smithery

To install usgs-water-mcp for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@pgiffy/usgs-water-mcp):

```bash
npx -y @smithery/cli install @pgiffy/usgs-water-mcp --client claude
```

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
         "args": ["/path/to/usgs-water-mcp/instantaneous.py"]
       }
     }
   }
   ```

3. Restart Claude Desktop

## Available Tools

### fetch_usgs_data

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

## Troubleshooting

### Common Issues

1. **API Connection Errors**: Ensure you have an active internet connection and the USGS API is accessible
2. **Invalid Site Numbers**: Verify site numbers exist using the USGS Water Data for the Nation website
3. **No Data Available**: Some sites may not have data for the requested time period or parameters
4. **Rate Limiting**: The USGS API has usage limits; avoid making too many requests in quick succession

### Finding Site Numbers

Use the [USGS Water Data for the Nation](https://waterdata.usgs.gov/nwis) website to find monitoring station site numbers in your area of interest.
