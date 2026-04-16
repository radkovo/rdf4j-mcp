"""
FitLayout MCP HTTP Server

Run:
    cd src && python server.py
or:
    cd src && uvicorn server:app --host 0.0.0.0 --port 8765 --reload

MCP endpoint: http://localhost:8765/mcp  (StreamableHTTP POST)
"""

from mcp.server.fastmcp import FastMCP
from tools import register_tools

mcp = FastMCP(
    name="rdf4j-mcp",
    host="127.0.0.1",    # override with FASTMCP_HOST env var
    port=8765,           # override with FASTMCP_PORT env var
    stateless_http=True, # each SPARQL request is independent
)

register_tools(mcp)

# ASGI app for uvicorn / gunicorn
app = mcp.streamable_http_app()

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
