from mcp.server.fastmcp import FastMCP
from water_data_api import register_water_data_tools
from flood_impact_api import register_flood_impact_tools
from ogc_api import register_ogc_tools

mcp = FastMCP("usgs_water_mcp")

register_water_data_tools(mcp)
register_flood_impact_tools(mcp)
register_ogc_tools(mcp)

if __name__ == "__main__":
    mcp.run(transport='stdio')