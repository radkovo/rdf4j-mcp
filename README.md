RDF4j MCP proxy
===============

(c) 2026 Radek Burget (burgetr@fit.vut.cz)

A Python MCP (Model Context Protocol) HTTP server that exposes RDF4j SPARQL query tools.

## Setup

```bash
pip install -r requirements.txt
```

To override the default RDF4j endpoint (`http://localhost:8400/api`) and repository (`default`),
create `src/config_local.py`:

```python
RDF4J_ENDPOINT = "https://any.server.com/rdf4j-server"
RDF4J_REPOSITORY = "repo"
RDF4J_USER = "..."
RDF4J_PASSWORD = "..."
```

## Running the server

```bash
cd src && python server.py
```

Or with uvicorn directly (supports `--reload` for development):

```bash
cd src && uvicorn server:app --host 0.0.0.0 --port 8765 --reload
```

The MCP endpoint will be available at `http://localhost:8765/mcp` (StreamableHTTP POST).

The host and port can be overridden via environment variables:

```bash
FASTMCP_HOST=0.0.0.0 FASTMCP_PORT=9000 python server.py
```

## Testing with the MCP inspector

```bash
cd src && mcp dev server.py
```

## Connecting from Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "rdf4j": {
      "url": "http://localhost:8765/mcp"
    }
  }
}
```
