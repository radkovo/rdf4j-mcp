import json
from typing import Annotated
from mcp.server.fastmcp import FastMCP
from pydantic import Field
from config import rdfClient


def register_tools(mcp: FastMCP) -> None:
    """Register all tools. Add new tools here."""

    @mcp.tool(description="Get the current FitLayout repository ID.")
    def repository_id() -> str:
        return rdfClient.repository_id

    @mcp.tool(
        description=(
            "Execute a SPARQL SELECT query against the FitLayout repository. "
            "Returns results in SPARQL JSON format (variable bindings)."
        )
    )
    def select_query(
        query: Annotated[str, Field(description="SPARQL SELECT query string, including PREFIX declarations.")],
        limit: Annotated[int, Field(description="Maximum number of results to return.")] = 2000,
        offset: Annotated[int, Field(description="Number of results to skip, for pagination.")] = 0,
        distinct: Annotated[bool, Field(description="Whether to apply DISTINCT to the query.")] = False,
    ) -> str:
        result = rdfClient.exec_sparql_query(query, limit, offset, distinct)
        return json.dumps(result, ensure_ascii=False)
