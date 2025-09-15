# California Ontology Documentation

## Overview
This ontology models California's geographical regions, cities, and their relationships. It is based on the 10 official tourism regions of California and includes cities with their population and area data.

## Namespace
- **Base IRI**: `http://www.semanticweb.org/california-ontology#`
- **Prefix**: `ca:`

## Class Hierarchy

### 1. GeographicalEntity (Top-level class)
The root class for all geographical entities in California.

#### Subclasses:

##### 1.1 Region
Represents geographical regions of California.

**Subclasses:**
- **NorthernRegion**: Regions in Northern California
- **CentralRegion**: Regions in Central California
- **SouthernRegion**: Regions in Southern California

##### 1.2 City
Represents cities in California.

**Subclasses:**
- **MajorCity**: Cities with population > 500,000
- **MediumCity**: Cities with population between 100,000 and 500,000
- **SmallCity**: Cities with population < 100,000

##### 1.3 County
Represents California counties (for future extension).

##### 1.4 Landmark
Represents notable landmarks (for future extension).

## Properties

### Object Properties (3)

1. **locatedIn**
   - Domain: City
   - Range: Region
   - Description: Links a city to the region it is located in

2. **hasCity**
   - Domain: Region
   - Range: City
   - Description: Links a region to cities within it (inverse of locatedIn)

3. **borders**
   - Domain: Region
   - Range: Region
   - Type: Symmetric Property
   - Description: Indicates two regions share a border

### Data Properties (3)

1. **hasPopulation**
   - Domain: GeographicalEntity
   - Range: xsd:integer
   - Description: The population count

2. **hasArea**
   - Domain: GeographicalEntity
   - Range: xsd:float
   - Description: The area in square kilometers

3. **establishedYear**
   - Domain: City
   - Range: xsd:integer
   - Description: The year the city was established

## Instances

### Regions (10 instances)
Based on California's official tourism regions from the provided map:

1. **NorthCoast** (NorthernRegion) - Northwestern coastal region
2. **ShastaCascades** (NorthernRegion) - Northeastern mountain region
3. **SacramentoValley** (NorthernRegion) - Northern central valley
4. **GoldCountry** (CentralRegion) - Historic gold rush region
5. **BayArea** (CentralRegion) - San Francisco Bay region
6. **SierraNevada** (CentralRegion) - Eastern mountain region
7. **SanJoaquinValley** (CentralRegion) - Southern central valley
8. **CentralCoast** (CentralRegion) - Central coastal region
9. **Desert** (SouthernRegion) - Southeastern desert region
10. **SouthernCalifornia** (SouthernRegion) - Southern metropolitan region

### Cities (12 instances)

#### Major Cities (Population > 500,000):
1. **Los Angeles** - Located in Southern California
   - Population: 3,898,747
   - Area: 1,302 km²
   - Established: 1781

2. **San Diego** - Located in Southern California
   - Population: 1,386,932
   - Area: 964.5 km²
   - Established: 1769

3. **San Jose** - Located in Bay Area
   - Population: 1,013,240
   - Area: 469.7 km²
   - Established: 1777

4. **San Francisco** - Located in Bay Area
   - Population: 873,965
   - Area: 121.5 km²
   - Established: 1776

#### Medium Cities (Population 100,000-500,000):
5. **Sacramento** - Located in Sacramento Valley
   - Population: 524,943
   - Area: 253 km²
   - Established: 1850

6. **Fresno** - Located in San Joaquin Valley
   - Population: 542,107
   - Area: 297 km²
   - Established: 1872

7. **Bakersfield** - Located in San Joaquin Valley
   - Population: 383,579
   - Area: 384.2 km²
   - Established: 1869

8. **Oakland** - Located in Bay Area
   - Population: 433,031
   - Area: 202 km²
   - Established: 1852

#### Small Cities (Population < 100,000):
9. **Santa Cruz** - Located in Central Coast
   - Population: 65,263
   - Area: 41 km²
   - Established: 1866

10. **Palm Springs** - Located in Desert
    - Population: 44,575
    - Area: 245 km²
    - Established: 1938

11. **Eureka** - Located in North Coast
    - Population: 26,710
    - Area: 37.4 km²
    - Established: 1850

12. **Redding** - Located in Shasta Cascades
    - Population: 93,611
    - Area: 158.4 km²
    - Established: 1887

## Border Relationships
The following regions border each other:
- North Coast ↔ Shasta Cascades
- North Coast ↔ Sacramento Valley
- Shasta Cascades ↔ Sacramento Valley
- Sacramento Valley ↔ Gold Country
- Sacramento Valley ↔ Bay Area
- Gold Country ↔ Sierra Nevada
- Bay Area ↔ Central Coast
- Bay Area ↔ San Joaquin Valley
- Sierra Nevada ↔ San Joaquin Valley
- San Joaquin Valley ↔ Central Coast
- San Joaquin Valley ↔ Desert
- Central Coast ↔ Southern California
- Desert ↔ Southern California

## SPARQL Queries

### Query 1: Complex Query
**Description**: Find cities in Central regions with population > 100,000 and area < 500 km²
```sparql
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
```
**Results**: Returns 5 cities including San Jose, San Francisco, Fresno, Oakland, and Bakersfield.

### Query 2: Type Restriction
**Description**: Find all instances that are exactly of type MajorCity
```sparql
SELECT ?city ?name ?population
WHERE {
  ?city rdf:type ca:MajorCity .
  ?city rdfs:label ?name .
  ?city ca:hasPopulation ?population .
}
```
**Results**: Returns 4 major cities: Los Angeles, San Diego, San Jose, and San Francisco.

### Query 3: Subclass Query
**Description**: Find all cities including subclasses
```sparql
SELECT ?city ?cityName ?type
WHERE {
  ?city rdf:type ?type .
  ?type rdfs:subClassOf* ca:City .
  ?city rdfs:label ?cityName .
}
```
**Results**: Returns all 12 cities with their specific types (MajorCity, MediumCity, or SmallCity).

### Query 4: SPARQL 1.1 Feature - Property Paths
**Description**: Find regions reachable from Bay Area through one or more border relationships
```sparql
SELECT DISTINCT ?region ?regionName
WHERE {
  ca:BayArea ca:borders+ ?region .
  ?region rdfs:label ?regionName .
}
```
**Results**: Returns 4 regions that can be reached from Bay Area: Central Coast, Southern California, San Joaquin Valley, and Desert.

### Query 5: Bordering Regions and Cities
**Description**: Find pairs of bordering regions and list cities in the first region
```sparql
SELECT ?region1Name ?region2Name ?cityName
WHERE {
  ?region1 ca:borders ?region2 .
  ?region1 rdfs:label ?region1Name .
  ?region2 rdfs:label ?region2Name .
  ?city ca:locatedIn ?region1 .
  ?city rdfs:label ?cityName .
  FILTER(STR(?region1) < STR(?region2))
}
```
**Results**: Returns bordering region pairs with cities, showing geographical relationships.

## Technical Details

- **Format**: RDF/XML (OWL)
- **File**: `california.owl`
- **Total Classes**: 11 (including subclasses)
- **Total Properties**: 6 (3 object properties, 3 data properties)
- **Total Instances**: 22 (10 regions + 12 cities)
- **Validation**: Successfully tested with RDFlib and SPARQL queries
