import csv
import io
from typing import Annotated
from mcp.server.fastmcp import FastMCP
from pydantic import Field
from config import rdfClient

_prefixes: dict | None = None

def _get_prefixes() -> dict:
    global _prefixes
    if _prefixes is None:
        _prefixes = rdfClient.get_prefixes()
    return _prefixes

def shorten(value: str, type_: str) -> str:
    if type_ == "uri":
        for ns, prefix in _get_prefixes().items():
            if value.startswith(ns):
                return prefix + value[len(ns):]
    elif type_ == "bnode":
        return "_:" + value
    return value

def sparql_to_csv(result: dict) -> str:
    vars_ = result["head"]["vars"]
    rows = result["results"]["bindings"]
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(vars_)
    for row in rows:
        writer.writerow([
            shorten(row[v]["value"], row[v]["type"]) if v in row else ""
            for v in vars_
        ])
    return buf.getvalue()

def _prefix_declarations() -> str:
    lines = [f"PREFIX {prefix} <{ns}>" for ns, prefix in _get_prefixes().items()]
    return "\n".join(lines)

def register_tools(mcp: FastMCP) -> None:
    """Register all tools. Add new tools here."""

    @mcp.tool(description="Get the current repository ID.")
    def repository_id() -> str:
        return rdfClient.repository_id

    prefix_block = _prefix_declarations()
    @mcp.tool(
        description=(
            "Execute a SPARQL SELECT query against the repository. "
            "Returns results as CSV with namespace prefixes applied to URI values. "
            f"The following prefixes are defined in the repository and may be used in queries:\n{prefix_block}"
        )
    )
    def select_query(
        query: Annotated[str, Field(description="SPARQL SELECT query string, including PREFIX declarations.")],
        limit: Annotated[int, Field(description="Maximum number of results to return.")] = 2000,
        offset: Annotated[int, Field(description="Number of results to skip, for pagination.")] = 0,
        distinct: Annotated[bool, Field(description="Whether to apply DISTINCT to the query.")] = False,
    ) -> str:
        result = rdfClient.exec_sparql_query(query, limit, offset, distinct)
        return sparql_to_csv(result)
