# ##################################################
# This a globe function which revolves around many
# functions in space.
# Call all the different functions
# @ Author : Rituraj Singh
#            rituraj.singh@irisa.fr
# Created Time : 18 July 2018, 17 : 45 (GMT + 2)
#         At: INRIA/IRISA, Rennes, France
# 1 : Maximum Relationship
# 0 : No Relationship
# <0,......1>
####################################################
import numpy as np
import pandas as pd
import time
import nltk
from nltk.corpus import wordnet as wn
from itertools import product
from operator import is_not
from functools import partial
from sklearn.utils.extmath import softmax

from numpy.core.multiarray import ndarray

from Planet_link import planet_link
from planet_property import find_planet_property
from Same_planet import find_same_planet
from Data_visualization import data_plot
from Subject_planet import find_planet_subjects
from Compare_subject_planet import compare_planet_subjects

from normalize_array import normalize_array


keywords_val = np.array(
    ['Hindi', 'English', 'India', 'France', 'Hindi', 'French_language', 'Narendra_Modi', 'Emmanuel_Macron', 'Pear', 'Mango','Sachin_Tendulkar','Paul_Pogba']);

####*####*####*####*####*#####*#####*#####*#####*#####*#####*####*####*#####
# -------------------------Black Hole----------------------------------------
# Extracting link property between two planets
# Note : Link Property are not symmetric
####*####*####*####*####*#####*#####*#####*#####*#####*#####*####*####*#####
array_planet_link = np.zeros((len(keywords_val), len(keywords_val)),dtype=int);
for x in range(0, keywords_val.size):
    for y in range(0,keywords_val.size):
        planets_knot = planet_link(keywords_val[x], keywords_val[y]);
        # print('Distance between',keywords_val[x], 'and',keywords_val[y],'is',planets_knot);
        if array_planet_link[y,x] != 0:
            array_planet_link[x,y] = array_planet_link[y,x] + planets_knot.size;
            array_planet_link[y,x] = array_planet_link[x,y];
        else:
            array_planet_link[x,y] = array_planet_link[x,y] + planets_knot.size;
            array_planet_link[y,x] = array_planet_link[x,y];
# df = pd.DataFrame(array_planet_link, columns=keywords_val, index=keywords_val);
# print(df.to_string())
# print("######################")
####*####*####*####*####*#####*#####*#####*#####*#####*#####*####*####*#####
# ------------------------Black Hole-----------------------------------------
# Check Same as planet
####*####*####*####*####*#####*#####*#####*#####*#####*#####*####*####*#####
array_same_planet = np.zeros((len(keywords_val), len(keywords_val)),dtype=float);
for x in range(0, keywords_val.size):
    for y in range(0,keywords_val.size):
        planet_same_first = find_same_planet(keywords_val[x]);
        planet_same_second = find_same_planet(keywords_val[y]);
        planets_knot = np.intersect1d(planet_same_first,planet_same_second);
        if planets_knot.size > 0:
            array_same_planet[x,y] = array_same_planet[x,y] + 1;
# df_1 = pd.DataFrame(array_same_planet, columns=keywords_val, index=keywords_val);
# print(df_1.to_string());
# print("######################")
####*####*####*####*####*#####*#####*#####*#####*#####*#####*####*####*#####
# -------------------------Black Hole----------------------------------------
####*####*####*####*####*#####*#####*#####*#####*#####*#####*####*####*#####
array_planet_property = np.zeros((len(keywords_val), len(keywords_val)), dtype=int);
for x in range(0, keywords_val.size):
    for y in range(x, keywords_val.size):
        if x == y:
            array_planet_property[y, x] = 0;
        else:
            planet_property_first = find_planet_property(keywords_val[x]);
            planet_property_second = find_planet_property(keywords_val[y]);
            planets_knot_property = np.intersect1d(planet_property_first, planet_property_second);
            class_thing = ['http://dbpedia.org/class/yago/Object100002684',
                           'http://dbpedia.org/class/yago/PhysicalEntity100001930',
                           'http://www.w3.org/2002/07/owl#Thing'];
            planets_knot_property = np.setdiff1d(planets_knot_property,class_thing);
            if planets_knot_property.size > 0:
                # print('The intersection for',keywords_val[x],'and', keywords_val[y],':\n')
                # print(planets_knot_property);
                # print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
                array_planet_property[x, y] = planets_knot_property.size;
                array_planet_property[y, x] = planets_knot_property.size;
# df_2 = pd.DataFrame(array_planet_property, columns=keywords_val, index=keywords_val);
# print(df_2.to_string());
# print("######################");

####*####*####*####*####*#####*#####*#####*#####*#####*#####*####*####*########
# -------------------------Black Hole----------------------------------------
# -------------------------Search Relation in Category Tree-------------------
####*####*####*####*####*#####*#####*#####*#####*#####*#####*####*####*########
# start_time = time.time();
# array_planetSubject_LowestMatch = np.zeros((len(keywords_val), len(keywords_val)), dtype=int);
# for x in range(0, keywords_val.size):
#     for y in range(x, keywords_val.size):
#         # print('Now Comparing', x, 'and', y);
#         if x == y:
#             array_planetSubject_LowestMatch[y, x] = 99;
#         else:
#             planet_subjects_first = find_planet_subjects(keywords_val[x]);
#             planet_subjects_second = find_planet_subjects(keywords_val[y]);
#             a = np.array([planet_subjects_first.size, planet_subjects_second.size]);
#             max_index = np.where(a == a.max());
#             if max_index == 0:
#                 larger_subject = planet_subjects_first;
#                 smaller_subject = planet_subjects_second;
#             else:
#                 larger_subject = planet_subjects_second;
#                 smaller_subject = planet_subjects_first;
#             matrix_commonSubject = np.nan * np.ones((larger_subject.size, smaller_subject.size), dtype=int)
#             for u in range(0,  larger_subject.size):
#                 for v in range(0, smaller_subject.size):
#                     common_satellites = compare_planet_subjects(larger_subject[u], smaller_subject[v]);
#                    # print('The intersection label of ',larger_subject[u], 'and', smaller_subject[v], 'is',common_satellites);
#                     if common_satellites is not None:
#                         matrix_commonSubject[u, v] = common_satellites;
#                     else:
#                         matrix_commonSubject[u, v] = 999;
#             # Find Lowest level match : Find Lowest value in matrix_commonSubject
#             lowest_labelMatch = min(map(min, matrix_commonSubject));
#             if lowest_labelMatch == 999:
#                 lowest_labelMatch = 0;
#             array_planetSubject_LowestMatch[x, y] = lowest_labelMatch;
#             array_planetSubject_LowestMatch[y, x] = lowest_labelMatch;
# # print(array_planet_property);
# df = pd.DataFrame(array_planetSubject_LowestMatch, columns=keywords_val, index=keywords_val);
# print(df);
# print("######################")
# elapsed_time = time.time() - start_time
# print(time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))

####*####*####*####*####*#####*#####*#####*#####*#####*#####*####*####*#####
# -------------------------Black Hole----------------------------------------
####*####*####*####*####*#####*#####*#####*#####*#####*#####*####*####*#####


#########@@#####################WORDNET#########@@#############################

####*####*####*####*####*#####*#####*#####*#####*#####*#####*####*####*#####
# -------------------------Black Hole----------------------------------------
####*####*####*####*####*#####*#####*#####*#####*#####*#####*####*####*#####
# array_wordnetMatch = np.zeros((len(keywords_val), len(keywords_val)), dtype=float);
# listSim = [];
# myList1 = keywords_val;
# myList2 = keywords_val;
# for x in range(0, keywords_val.size):
#     for y in range(x, keywords_val.size):
#         print('Now Comparing', keywords_val[x], 'and', keywords_val[y]);
#         if x == y:
#             array_wordnetMatch[y, x] = 1;
#         else:
#             list1 = wn.synsets((keywords_val[x]));
#             list2 = wn.synsets(keywords_val[y]);
#             sList = [ss1.path_similarity(ss2) for ss1, ss2 in product(list1, list2)]
#             sListFilter = ([l for l in sList if l is not None])
#             if not sListFilter:
#                 sListFilter.append(0);
#             best = sorted(sListFilter, reverse=True)[0]
#             array_wordnetMatch[x, y] = best;
#             array_wordnetMatch[y, x] = best;
# df = pd.DataFrame(array_wordnetMatch, columns=keywords_val, index=keywords_val);
# print(df);

####*####*####*####*####*#####*#####*#####*#####*#####*#####*####*####*#####
# -------------------------Black Hole----------------------------------------
####*####*####*####*####*#####*#####*#####*#####*#####*#####*####*####*#####

####################################################################################################################
#----------------------------------------------Array Processing-----------------------------------------------------
####################################################################################################################
# The below code normalizes the array in the range of 0 and 1
normalized_array_planet_link = normalize_array(array_planet_link);
# soft_array_planet_link = softmax(array_planet_link);
# print((pd.DataFrame(normalized_array_planet_link, columns=keywords_val, index=keywords_val)).round(3).to_string());


norm_array_planet_property = normalize_array(array_planet_property);
# print((pd.DataFrame(norm_array_planet_property, columns=keywords_val, index=keywords_val)).round(3).to_string());

scaled_weight = np.array([[0.6, 0.4]]);
scaled_matrix = np.dot(scaled_weight[0,0], normalized_array_planet_link) + np.dot(scaled_weight[0, 1], norm_array_planet_property);
print(((pd.DataFrame(scaled_matrix, columns=keywords_val, index=keywords_val)).round(3)).to_string())
# Add the Same word weights here
for loop1 in range(array_same_planet.shape[0]):
    for loop2 in range(loop1, array_same_planet.shape[0]):
        # print('The value are', array_same_planet[loop1, loop2]);
        if (array_same_planet[loop1, loop2] == 1.0) & (loop1 != loop2):
            print('I am here', loop1, loop2, '\n')
            scaled_matrix[loop1, loop2] = 1.0;
            scaled_matrix[loop2, loop1] = 1.0;
print(((pd.DataFrame(scaled_matrix, columns=keywords_val, index=keywords_val)).round(3)).to_string())

data_plot(scaled_matrix.round(3), keywords_val);



# norm_scaled_matrix = normalize_array(scaled_matrix);
# print(((pd.DataFrame(norm_scaled_matrix, columns=keywords_val, index=keywords_val)).round(3)).to_string())
# soft_weights = np.empty(scaled_matrix.shape, dtype=float);
# for temp in range(scaled_matrix.shape[0]):
#     soft_weights[temp] = ((np.exp(scaled_matrix[temp, :]))/(np.sum(np.exp(scaled_matrix[temp, :]))))
# print('Final Soft Weights \n')
# print(((pd.DataFrame(soft_weights, columns=keywords_val, index=keywords_val)).round(3)).to_string())