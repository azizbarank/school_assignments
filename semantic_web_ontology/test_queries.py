from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery

# Load the ontology
g = Graph()
g.parse("project.owl", format="xml")

print("=" * 60)
print("Testing SPARQL Queries on California Ontology")
print("=" * 60)

# Define queries
queries = [
    {
        "name": "Query 1: Complex query - Cities in Central regions with population > 100k and area < 500 km²",
        "query": """
            PREFIX ca: <http://www.semanticweb.org/california-ontology#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT ?city ?cityName ?population ?area ?region
            WHERE {
              ?city rdf:type/rdfs:subClassOf* ca:City .
              ?city rdfs:label ?cityName .
              ?city ca:hasPopulation ?population .
              ?city ca:hasArea ?area .
              ?city ca:locatedIn ?region .
              ?region rdf:type ca:CentralRegion .
              FILTER(?population > 100000 && ?area < 500)
            }
            ORDER BY DESC(?population)
        """
    },
    {
        "name": "Query 2: Find all MajorCity instances",
        "query": """
            PREFIX ca: <http://www.semanticweb.org/california-ontology#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT ?city ?name ?population
            WHERE {
              ?city rdf:type ca:MajorCity .
              ?city rdfs:label ?name .
              ?city ca:hasPopulation ?population .
            }
            ORDER BY DESC(?population)
        """
    },
    {
        "name": "Query 3: Find all cities (including subclasses)",
        "query": """
            PREFIX ca: <http://www.semanticweb.org/california-ontology#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT ?city ?cityName ?type
            WHERE {
              ?city rdf:type ?type .
              ?type rdfs:subClassOf* ca:City .
              ?city rdfs:label ?cityName .
            }
            ORDER BY ?type ?cityName
        """
    },
    {
        "name": "Query 4: SPARQL 1.1 - Property paths (regions reachable from Bay Area)",
        "query": """
            PREFIX ca: <http://www.semanticweb.org/california-ontology#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT DISTINCT ?region ?regionName
            WHERE {
              ca:BayArea ca:borders+ ?region .
              ?region rdfs:label ?regionName .
            }
        """
    },
    {
        "name": "Query 5: Bordering regions and their cities",
        "query": """
            PREFIX ca: <http://www.semanticweb.org/california-ontology#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT ?region1Name ?region2Name ?cityName
            WHERE {
              ?region1 ca:borders ?region2 .
              ?region1 rdfs:label ?region1Name .
              ?region2 rdfs:label ?region2Name .
              ?city ca:locatedIn ?region1 .
              ?city rdfs:label ?cityName .
              FILTER(STR(?region1) < STR(?region2))
            }
            ORDER BY ?region1Name ?region2Name ?cityName
            LIMIT 20
        """
    }
]

# Execute and display results for each query
for i, q in enumerate(queries, 1):
    print(f"\n{q['name']}")
    print("-" * 60)

    try:
        qres = g.query(q['query'])

        # Print results
        if len(qres) == 0:
            print("No results found.")
        else:
            # Get column headers from the first result
            headers = list(qres.bindings[0].keys()) if qres.bindings else []

            # Print headers
            if headers:
                header_str = " | ".join([str(h) for h in headers])
                print(header_str)
                print("-" * len(header_str))

            # Print rows
            for row in qres:
                row_values = []
                for var in headers:
                    val = row[var]
                    # Format the value
                    if hasattr(val, 'value'):
                        row_values.append(str(val.value))
                    else:
                        # Extract just the fragment from URIs
                        val_str = str(val)
                        if '#' in val_str:
                            val_str = val_str.split('#')[-1]
                        row_values.append(val_str)
                print(" | ".join(row_values))

        print(f"\nTotal results: {len(qres)}")

    except Exception as e:
        print(f"Error executing query: {e}")

print("\n" + "=" * 60)
print("Query testing complete!")
print("=" * 60)