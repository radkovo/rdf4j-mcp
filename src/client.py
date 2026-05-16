import requests
import base64

class Rdf4jClient:
    """ REST client for RDF4j server. """

    def __init__(self, api_root, repository_id):
        self.api_root = api_root
        self.repository_id = repository_id
        self.username = None
        self.password = None

    def login(self, username, password):
        self.username = username
        self.password = password
    
    def repo_endpoint(self):
        return f"{self.api_root}/repositories/{self.repository_id}"
    
    def _auth_headers(self):
        if self.username and self.password:
            authstring = f"{self.username}:{self.password}"
            return {"Authorization": f"Basic {base64.b64encode(authstring.encode()).decode()}"}
        return {}

    def exec_sparql_query(self, query, limit=50000, offset=0, distinct=False):
        """ Executes a SPARQL SELECT query on the repository and returns the bindings. """
        url = f"{self.repo_endpoint()}?limit={limit}&offset={offset}"
        if distinct:
            url += "&distinct=true"
        headers = {
            "Content-Type": "application/sparql-query",
            "Accept": "application/sparql-results+json",
            **self._auth_headers(),
        }
        response = requests.post(url, data=query, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_prefixes(self):
        """Retrieves the repository's namespace prefixes.

        Returns a dict mapping namespace URI to prefixed name, e.g.
        {"http://www.w3.org/1999/02/22-rdf-syntax-ns#": "rdf:"}.
        """
        url = f"{self.repo_endpoint()}/namespaces"
        headers = {
            "Accept": "application/sparql-results+json",
            **self._auth_headers(),
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return {
            row["namespace"]["value"]: row["prefix"]["value"] + ":"
            for row in data["results"]["bindings"]
        }
