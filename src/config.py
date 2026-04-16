from client import Rdf4jClient

# Disable IPv6 support if necessary (e.g. for the server running in docker containers)
import requests
requests.packages.urllib3.util.connection.HAS_IPV6 = False

# Default server configuration; override in config_local.py (not versioned, see .gitignore)
RDF4J_ENDPOINT = "https://localhost/rdf4j-server"
RDF4J_REPOSITORY = "default"
RDF4J_USER = None
RDF4J_PASSWORD = None

try:
    from config_local import RDF4J_ENDPOINT, RDF4J_REPOSITORY, RDF4J_USER, RDF4J_PASSWORD
except ImportError:
    pass

rdfClient = Rdf4jClient(RDF4J_ENDPOINT, RDF4J_REPOSITORY)
if RDF4J_USER and RDF4J_PASSWORD:
    rdfClient.login(RDF4J_USER, RDF4J_PASSWORD)
