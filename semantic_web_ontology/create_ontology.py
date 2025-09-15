from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal, URIRef
from rdflib.namespace import XSD

# Create a new graph
g = Graph()

# Define namespace for our California ontology
CA = Namespace("http://www.semanticweb.org/california-ontology#")
g.bind("ca", CA)
g.bind("owl", OWL)
g.bind("rdfs", RDFS)
g.bind("rdf", RDF)
g.bind("xsd", XSD)

# Define the ontology itself
ontology = CA[""]
g.add((ontology, RDF.type, OWL.Ontology))
g.add((ontology, RDFS.label, Literal("California Ontology")))
g.add((ontology, RDFS.comment, Literal("An ontology describing California's regions, cities, and their properties")))

# ============== CLASSES ==============
# Top-level class
g.add((CA.GeographicalEntity, RDF.type, OWL.Class))
g.add((CA.GeographicalEntity, RDFS.label, Literal("Geographical Entity")))
g.add((CA.GeographicalEntity, RDFS.comment, Literal("Any geographical entity in California")))

# Region classes
g.add((CA.Region, RDF.type, OWL.Class))
g.add((CA.Region, RDFS.subClassOf, CA.GeographicalEntity))
g.add((CA.Region, RDFS.label, Literal("Region")))

g.add((CA.NorthernRegion, RDF.type, OWL.Class))
g.add((CA.NorthernRegion, RDFS.subClassOf, CA.Region))
g.add((CA.NorthernRegion, RDFS.label, Literal("Northern Region")))

g.add((CA.CentralRegion, RDF.type, OWL.Class))
g.add((CA.CentralRegion, RDFS.subClassOf, CA.Region))
g.add((CA.CentralRegion, RDFS.label, Literal("Central Region")))

g.add((CA.SouthernRegion, RDF.type, OWL.Class))
g.add((CA.SouthernRegion, RDFS.subClassOf, CA.Region))
g.add((CA.SouthernRegion, RDFS.label, Literal("Southern Region")))

# City classes
g.add((CA.City, RDF.type, OWL.Class))
g.add((CA.City, RDFS.subClassOf, CA.GeographicalEntity))
g.add((CA.City, RDFS.label, Literal("City")))

g.add((CA.MajorCity, RDF.type, OWL.Class))
g.add((CA.MajorCity, RDFS.subClassOf, CA.City))
g.add((CA.MajorCity, RDFS.label, Literal("Major City")))
g.add((CA.MajorCity, RDFS.comment, Literal("City with population over 500,000")))

g.add((CA.MediumCity, RDF.type, OWL.Class))
g.add((CA.MediumCity, RDFS.subClassOf, CA.City))
g.add((CA.MediumCity, RDFS.label, Literal("Medium City")))
g.add((CA.MediumCity, RDFS.comment, Literal("City with population between 100,000 and 500,000")))

g.add((CA.SmallCity, RDF.type, OWL.Class))
g.add((CA.SmallCity, RDFS.subClassOf, CA.City))
g.add((CA.SmallCity, RDFS.label, Literal("Small City")))
g.add((CA.SmallCity, RDFS.comment, Literal("City with population under 100,000")))

# Additional classes
g.add((CA.County, RDF.type, OWL.Class))
g.add((CA.County, RDFS.subClassOf, CA.GeographicalEntity))
g.add((CA.County, RDFS.label, Literal("County")))

g.add((CA.Landmark, RDF.type, OWL.Class))
g.add((CA.Landmark, RDFS.subClassOf, CA.GeographicalEntity))
g.add((CA.Landmark, RDFS.label, Literal("Landmark")))

# ============== OBJECT PROPERTIES ==============
# locatedIn property
g.add((CA.locatedIn, RDF.type, OWL.ObjectProperty))
g.add((CA.locatedIn, RDFS.domain, CA.City))
g.add((CA.locatedIn, RDFS.range, CA.Region))
g.add((CA.locatedIn, RDFS.label, Literal("located in")))

# hasCity property (inverse of locatedIn)
g.add((CA.hasCity, RDF.type, OWL.ObjectProperty))
g.add((CA.hasCity, RDFS.domain, CA.Region))
g.add((CA.hasCity, RDFS.range, CA.City))
g.add((CA.hasCity, OWL.inverseOf, CA.locatedIn))
g.add((CA.hasCity, RDFS.label, Literal("has city")))

# borders property
g.add((CA.borders, RDF.type, OWL.ObjectProperty))
g.add((CA.borders, RDF.type, OWL.SymmetricProperty))
g.add((CA.borders, RDFS.domain, CA.Region))
g.add((CA.borders, RDFS.range, CA.Region))
g.add((CA.borders, RDFS.label, Literal("borders")))

# ============== DATA PROPERTIES ==============
# hasPopulation property
g.add((CA.hasPopulation, RDF.type, OWL.DatatypeProperty))
g.add((CA.hasPopulation, RDFS.domain, CA.GeographicalEntity))
g.add((CA.hasPopulation, RDFS.range, XSD.integer))
g.add((CA.hasPopulation, RDFS.label, Literal("has population")))

# hasArea property
g.add((CA.hasArea, RDF.type, OWL.DatatypeProperty))
g.add((CA.hasArea, RDFS.domain, CA.GeographicalEntity))
g.add((CA.hasArea, RDFS.range, XSD.float))
g.add((CA.hasArea, RDFS.label, Literal("has area (km²)")))

# establishedYear property
g.add((CA.establishedYear, RDF.type, OWL.DatatypeProperty))
g.add((CA.establishedYear, RDFS.domain, CA.City))
g.add((CA.establishedYear, RDFS.range, XSD.integer))
g.add((CA.establishedYear, RDFS.label, Literal("established year")))

# ============== INSTANCES - REGIONS ==============
# Based on the map image
regions = [
    ("NorthCoast", CA.NorthernRegion, "North Coast"),
    ("ShastaCascades", CA.NorthernRegion, "Shasta Cascades"),
    ("SacramentoValley", CA.NorthernRegion, "Sacramento Valley"),
    ("GoldCountry", CA.CentralRegion, "Gold Country"),
    ("BayArea", CA.CentralRegion, "Bay Area"),
    ("SierraNevada", CA.CentralRegion, "Sierra Nevada"),
    ("SanJoaquinValley", CA.CentralRegion, "San Joaquin Valley"),
    ("CentralCoast", CA.CentralRegion, "Central Coast"),
    ("Desert", CA.SouthernRegion, "Desert"),
    ("SouthernCalifornia", CA.SouthernRegion, "Southern California")
]

for region_id, region_class, label in regions:
    region = CA[region_id]
    g.add((region, RDF.type, region_class))
    g.add((region, RDFS.label, Literal(label)))

# Add border relationships based on the map
g.add((CA.NorthCoast, CA.borders, CA.ShastaCascades))
g.add((CA.NorthCoast, CA.borders, CA.SacramentoValley))
g.add((CA.ShastaCascades, CA.borders, CA.SacramentoValley))
g.add((CA.SacramentoValley, CA.borders, CA.GoldCountry))
g.add((CA.SacramentoValley, CA.borders, CA.BayArea))
g.add((CA.GoldCountry, CA.borders, CA.SierraNevada))
g.add((CA.BayArea, CA.borders, CA.CentralCoast))
g.add((CA.BayArea, CA.borders, CA.SanJoaquinValley))
g.add((CA.SierraNevada, CA.borders, CA.SanJoaquinValley))
g.add((CA.SanJoaquinValley, CA.borders, CA.CentralCoast))
g.add((CA.CentralCoast, CA.borders, CA.SouthernCalifornia))
g.add((CA.SanJoaquinValley, CA.borders, CA.Desert))
g.add((CA.Desert, CA.borders, CA.SouthernCalifornia))

# ============== INSTANCES - CITIES ==============
# Major cities (>500k population)
cities_data = [
    # City ID, Type, Label, Region, Population, Area(km²), Year
    ("LosAngeles", CA.MajorCity, "Los Angeles", CA.SouthernCalifornia, 3898747, 1302.0, 1781),
    ("SanDiego", CA.MajorCity, "San Diego", CA.SouthernCalifornia, 1386932, 964.5, 1769),
    ("SanJose", CA.MajorCity, "San Jose", CA.BayArea, 1013240, 469.7, 1777),
    ("SanFrancisco", CA.MajorCity, "San Francisco", CA.BayArea, 873965, 121.5, 1776),

    # Medium cities (100k-500k)
    ("Sacramento", CA.MediumCity, "Sacramento", CA.SacramentoValley, 524943, 253.0, 1850),
    ("Fresno", CA.MediumCity, "Fresno", CA.SanJoaquinValley, 542107, 297.0, 1872),
    ("Bakersfield", CA.MediumCity, "Bakersfield", CA.SanJoaquinValley, 383579, 384.2, 1869),
    ("Oakland", CA.MediumCity, "Oakland", CA.BayArea, 433031, 202.0, 1852),

    # Small cities (<100k)
    ("SantaCruz", CA.SmallCity, "Santa Cruz", CA.CentralCoast, 65263, 41.0, 1866),
    ("PalmSprings", CA.SmallCity, "Palm Springs", CA.Desert, 44575, 245.0, 1938),
    ("Eureka", CA.SmallCity, "Eureka", CA.NorthCoast, 26710, 37.4, 1850),
    ("Redding", CA.SmallCity, "Redding", CA.ShastaCascades, 93611, 158.4, 1887)
]

for city_id, city_type, label, region, pop, area, year in cities_data:
    city = CA[city_id]
    g.add((city, RDF.type, city_type))
    g.add((city, RDFS.label, Literal(label)))
    g.add((city, CA.locatedIn, region))
    g.add((city, CA.hasPopulation, Literal(pop, datatype=XSD.integer)))
    g.add((city, CA.hasArea, Literal(area, datatype=XSD.float)))
    g.add((city, CA.establishedYear, Literal(year, datatype=XSD.integer)))

# Save as RDF/XML (OWL format)
g.serialize(destination="project.owl", format="xml")
print("Ontology created successfully as project.owl")

# Also save as Turtle for readability
g.serialize(destination="california_ontology.ttl", format="turtle")
print("Also saved as california_ontology.ttl for better readability")