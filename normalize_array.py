import numpy as np;


def normalize_array(var_matrix):
    normalized_matrix = (var_matrix - np.min(var_matrix)) / (np.max(var_matrix) - np.min(var_matrix))
    return normalized_matrix;
