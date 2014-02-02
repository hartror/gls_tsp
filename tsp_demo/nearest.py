import sys
from random import shuffle

import numpy

import tsplib
import plotting


def nearest_tour(distances, count, randomize=True):
    available = range(1, count)
    if randomize:
        shuffle(available)
    tour = [0]
    while available:
        nearest = numpy.argmin(distances[tour[-1]][available])
        tour.append(available[nearest])
        available.pop(nearest)
    solution = numpy.array(tour, dtype=numpy.int)
    cost = tsplib.calc_cost(solution, distances)
    return solution, cost


def main(argv):
    coords, distances = tsplib.load(argv[1])
    plot = plotting.TspPlot(coords)
    solution, cost = nearest_tour(distances, len(distances))
    plot.redraw_best(solution, cost)
    print cost
    while 1:
        pass


if __name__ == "__main__":
    main(sys.argv)
