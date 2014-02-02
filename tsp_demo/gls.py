import sys

import numpy

import tsplib
import plotting
from nearest import nearest_tour
from two_opt import two_opt


def main(argv):
    alpha = float(argv[1])
    coords, distances = tsplib.load(argv[2])
    count = len(distances)
    solution, best_cost = nearest_tour(distances, len(distances))
    plot = plotting.TspPlot(coords, draw_guess=True)
    print best_cost

    penalties = numpy.copy(distances)
    penalties[:] = 0.0

    def calc_cost(solution):
        cost = tsplib.calc_cost(solution, distances)
        sol_pens = penalties[solution[:-1], solution[1:]]
        gls_cost = (cost +
                    alpha *
                    (best_cost/count+1) *
                    (sol_pens.sum() + penalties[solution[-1], solution[0]]))
        return gls_cost

    def penalise(solution):
        sol_dists = distances[solution[0:-1], solution[1:]]
        sol_dists = numpy.append(sol_dists, (distances[solution[0], solution[-1]],))
        sol_pens = penalties[solution[0:-1], solution[1:]]
        sol_pens = numpy.append(sol_pens, (penalties[solution[0], solution[-1]],))
        utility = sol_dists/(sol_pens+1)
        index_a = numpy.argmax(utility)
        index_b = index_a+1 if index_a != count-1 else 0
        a = solution[index_a]
        b = solution[index_b] 
        penalties[a,b] += 1.0
        penalties[b,a] += 1.0

    def redraw_guess(solution, cost):
        cost = tsplib.calc_cost(solution, distances) # ugh
        plot.redraw_guess(solution, cost)

    gls_cost = cost = best_cost
    best_solution = numpy.copy(solution)
    plot.redraw_best(best_solution, cost)

    while 1:
        solution, gls_cost = two_opt(solution, gls_cost, len(distances), calc_cost, redraw_guess)
        cost = tsplib.calc_cost(solution, distances)
        if cost < best_cost:
            print cost
            best_cost = cost
            best_solution[:] = solution
            plot.redraw_best(best_solution, cost)
        penalise(solution)


if __name__ == '__main__':
    main(sys.argv)
