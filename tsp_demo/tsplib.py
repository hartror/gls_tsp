import re

import numpy
import scipy.spatial.distance


TSP_REGEX = r' *\d+ +(\d+\.?\d*) +(\d+\.?\d*)$'


def load(filename):
    coords = load_coords(filename)
    distances = calc_distances(coords)
    return coords, distances


def load_coords(filename):
    """
    Load a set of coordinates from a tsp file, ignoring lines that don't match TSP_REGEX.
    """
    with open(filename, 'r') as tsp_file:
        matches = (re.match(TSP_REGEX, line)
                   for line in tsp_file)
        coords = numpy.array(
            [vec_match.groups()
             for vec_match in matches
             if vec_match], dtype=float)
    return coords


def calc_distances(coords):
    """
    Calculate all the distance combinations for a [[x,y],...] matrix.
    This contains all the information twice for ease of indexing.
    """
    return numpy.rint(
        scipy.spatial.distance.squareform(
            scipy.spatial.distance.pdist(coords, 'euclidean')))


def calc_cost(solution, distances):
    """
    Calculate the cost of a full tour from solution[0] -> solution[0].
    Distances is a set of precalculated distances from calc_distances
    """
    cost = distances[solution[:-1], solution[1:]].sum()
    cost += distances[solution[-1], solution[0]]
    return cost
