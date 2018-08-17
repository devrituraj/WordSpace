# ###################################################
# Explore the direct inked entities between keywords
# Here direct linked entities states the one edge link
# between the two set of Keywords
# Input : Two keywords
# Output : Set of Linked Edges between the two keywords
#          The linked edges are the properties between the
#          two keywords.
# @ Author : Rituraj Singh
#            rituraj.singh@irisa.fr
# Created Time : 18 July 2018, 17 : 45 (GMT + 2)
#         At: INRIA/IRISA, Rennes, France
####################################################
from SPARQLWrapper import SPARQLWrapper, JSON
import numpy as np

sparql = SPARQLWrapper("http://dbpedia.org/sparql")


# print(query_str)
# Q1 : dbpedia:India dcterms:subject ?super


def find_planet_property(first_key):
    query_str = """
        PREFIX dbpedia: <http://dbpedia.org/resource/>
        PREFIX category: <http://dbpedia.org/resource/Category:>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX dcterms: <http://purl.org/dc/terms/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        select distinct ?super 
        where 
        {
            dbpedia:""" + first_key + """ rdf:type ?super
        }"""
    sparql.setQuery(query_str);
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    # print(results);
    my_key = [];
    for result in results['results']['bindings']:
        #   print(result['super']['value'])
        my_key.append(result['super']['value'])

    my_keywords = np.array(my_key)
    return my_keywords;
