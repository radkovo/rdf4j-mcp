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
    
    def exec_sparql_query(self, query, limit=50000, offset=0, distinct=False):
        """ Executes a SPARQL SELECT query on the repository and returns the bindings. """
        url = f"{self.repo_endpoint()}?limit={limit}&offset={offset}"
        if distinct:
            url += "&distinct=true"
        headers = { 
            "Content-Type": "application/sparql-query",
            "Accept": "application/sparql-results+json"
        }
        if self.username and self.password:
            authstring = f"{self.username}:{self.password}"
            headers["Authorization"] = f"Basic {base64.b64encode(authstring.encode()).decode()}"
        response = requests.post(url, data=query, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
