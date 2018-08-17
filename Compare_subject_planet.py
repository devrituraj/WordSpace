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
max_label_traverse = 2;

def compare_planet_labels(first_keyword, second_keyword, traverse_label):
    query_str = """
    PREFIX dbpedia: <http://dbpedia.org/resource/>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX dbc: <http://dbpedia.org/resource/Category:>
    select distinct ?super where {
        ?super (^skos:broader){0,""" + traverse_label + """} <""" + first_keyword + """>,<""" + second_keyword + """>
    }"""
    # print(query_str)
    sparql.setQuery(query_str);
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    # print(results);
    my_key = [];
    for result in results['results']['bindings']:
        # print(result['super']['value'])
        my_key.append(result['super']['value'])

    my_keywords = np.array(my_key)
    return my_keywords;


def compare_planet_subjects(first_keyword, second_keyword):
    for label_val in range(1, int(max_label_traverse)):
        common_satellites = compare_planet_labels(first_keyword, second_keyword, str(label_val));
        # print('value of Common Satellite : ', common_satellites);
        if common_satellites.size != 0:
            return label_val;


