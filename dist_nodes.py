from SPARQLWrapper import SPARQLWrapper, JSON
sparql = SPARQLWrapper("http://dbpedia.org/sparql");
query_str = """
    PREFIX dbpedia: <http://dbpedia.org/resource/>
    PREFIX category: <http://dbpedia.org/resource/Category:>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX dbo: <http://dbpedia.org/ontology/> 
   SELECT ?a ?b ?super (?aLength + ?bLength as ?length)
{
  values (?a ?b) { (dbpedia:Kolkata dbpedia:New_Delhi) }
  {
    SELECT ?a ?super (COUNT(?mid) as ?aLength) {
      ?a rdfs:subClassOf* ?mid .
      ?mid rdfs:subClassOf+ ?super .
    }
    GROUP BY ?a ?super
  }
  {
    SELECT ?b ?super (COUNT(?mid) as ?bLength) {
      ?b rdfs:subClassOf* ?mid .
      ?mid rdfs:subClassOf+ ?super .
    }
    GROUP BY ?b ?super
  }
}
ORDER BY ?length
LIMIT 1 """
sparql.setQuery(query_str);
sparql.setReturnFormat(JSON)
results = sparql.query().convert();
print(results);
print("\n")
#for result in results['results']['bindings']:
#    print(result['label']['value'])


for result in results["results"]["bindings"]:
    print(result["super"]["value"])

