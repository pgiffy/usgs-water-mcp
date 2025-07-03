#!/usr/bin/env python3
"""
HTTP wrapper for USGS Water MCP server to work with Smithery deployments.
"""

import os
import json
import asyncio
from typing import Dict, Any
from urllib.parse import parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler

class MCPHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self._tools_cache = None
        super().__init__(*args, **kwargs)
    
    def _get_tools(self):
        """Lazy load tools configuration"""
        if self._tools_cache is None:
            self._tools_cache = [
                {
                    "name": "fetch_usgs_data",
                    "description": "Fetch current water data from USGS for specified sites",
                    "parameters": {
                        "sites": "Comma-separated site numbers (e.g., '01646500' or '01646500,01647000')",
                        "parameter_codes": "Comma-separated parameter codes (e.g., '00060,00065')",
                        "start_date": "Start date in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM)",
                        "end_date": "End date in ISO format",
                        "period": "Period code (e.g., 'P7D' for 7 days)"
                    }
                }
            ]
        return self._tools_cache
    
    def do_GET(self):
        """Handle GET requests for tool discovery"""
        if self.path.startswith('/mcp'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Return available tools with lazy loading
            # Configuration parameters are ignored for tool discovery
            response = {
                "tools": self._get_tools()
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Handle POST requests for tool execution"""
        if self.path.startswith('/mcp'):
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                request_data = json.loads(post_data.decode())
                
                # Execute the tool
                result = asyncio.run(self._execute_tool(request_data))
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_response = {"error": str(e)}
                self.wfile.write(json.dumps(error_response).encode())
        else:
            self.send_error(404)
    
    def do_DELETE(self):
        """Handle DELETE requests"""
        if self.path.startswith('/mcp'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Return success response for DELETE
            response = {"status": "success"}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_error(404)
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    async def _execute_tool(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the requested tool"""
        tool_name = request_data.get('tool')
        params = request_data.get('parameters', {})
        
        if tool_name == 'fetch_usgs_data':
            # Lazy import of the actual implementation
            from current_water_levels import get_current_water_data_values
            
            sites = params.get('sites', '')
            parameter_codes = params.get('parameter_codes', '')
            start_date = params.get('start_date', '')
            end_date = params.get('end_date', '')
            period = params.get('period', '')
            
            result = await get_current_water_data_values(
                sites=sites,
                parameter_codes=parameter_codes if parameter_codes else None,
                start_date=start_date if start_date else None,
                end_date=end_date if end_date else None,
                period=period if period else None
            )
            
            return {"result": result}
        else:
            raise ValueError(f"Unknown tool: {tool_name}")

def run_server():
    """Run the HTTP server"""
    port = int(os.environ.get('PORT', 8000))
    server = HTTPServer(('0.0.0.0', port), MCPHandler)
    print(f"Starting server on port {port}")
    server.serve_forever()

if __name__ == "__main__":
    run_server()