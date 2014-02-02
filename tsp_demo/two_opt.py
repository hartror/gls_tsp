import sys

import numpy

import tsplib
import plotting
from nearest import nearest_tour

def two_opt(solution, cost, count, calc_cost, redraw_best):
    best_cost = cost = calc_cost(solution)
    improving = True
    while improving:
        improving = False
        for i in xrange(1, count-2):
            for j in xrange(i+1, count):
                # numpy magic!
                solution[i:j+1] = solution[j-count:i-count-1:-1]
                cost = calc_cost(solution)
                if cost < best_cost:
                    best_cost = cost
                    improving = True
                    redraw_best(solution, cost)
                else:
                    # more numpy magic!
                    solution[i:j+1] = solution[j-count:i-count-1:-1]
    return solution, cost


def main(argv):
    coords, distances = tsplib.load(argv[1])
    plot = plotting.TspPlot(coords)
    solution, cost = nearest_tour(distances, len(distances))
    print cost
    def calc_cost(solution):
        return tsplib.calc_cost(solution, distances)
    two_opt(solution, cost, len(distances), calc_cost, plot.redraw_best)
    while 1:
        pass


if __name__ == '__main__':
    main(sys.argv)
