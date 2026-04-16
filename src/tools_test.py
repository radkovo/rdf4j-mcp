from config import rdfClient

def select_query(query, limit, offset, distinct):
    return rdfClient.exec_sparql_query(query, limit, offset, distinct)

def test_select_query():
    # Test code
    query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT DISTINCT ?t
        WHERE {
            ?x rdf:type ?t
        }
    """

    result = select_query(query, 10, 0, False)
    print("Types:")
    for row in result["results"]["bindings"]:
        print(row["t"]["value"])

test_select_query()
