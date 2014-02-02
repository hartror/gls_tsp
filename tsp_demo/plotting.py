import numpy

import matplotlib.pyplot

COSTS_LENGTH = 100

class TspPlot(object):

    def __init__(self, coords, draw_guess=False):
        self.coords = coords
        self.draw_guess = draw_guess
        fig = matplotlib.pyplot.figure(figsize=(16, 10), dpi=100)

        self.cities = fig.add_subplot(211)
        x, y = self.coords[:,0], self.coords[:,1]
        _, self.best_line = self.cities.plot(
            x, y, 's', # cities
            x, y, '-') # best line

        if self.draw_guess:
            self.guess_line = self.cities.plot(
                x, y, '--')[0]

        self.x = 0
        self.costs = fig.add_subplot(212)
        self.x_costs = numpy.array(range(0, COSTS_LENGTH))
        self.best_costs = numpy.array([0]*COSTS_LENGTH)
        self.best_costs_line = self.costs.plot(
            self.x_costs, self.best_costs, '-')[0]

        if self.draw_guess:
            self.guess_costs = numpy.array([0]*COSTS_LENGTH)
            self.guess_costs_line = self.costs.plot(
                self.x_costs, self.guess_costs)[0]

        matplotlib.pyplot.ion()
        matplotlib.pyplot.show()

    def redraw_guess(self, solution, cost):
        self.update_guess_costs(cost)
        self.redraw_line(self.guess_line, solution)
    
    def redraw_best(self, solution, cost):
        self.update_best_costs(cost)
        self.redraw_line(self.best_line, solution)
    
    def redraw_line(self, line, solution):
        sol_coords = self.coords[solution]
        line.set_xdata(sol_coords[:,0])
        line.set_ydata(sol_coords[:,1])
        matplotlib.pyplot.draw()

    def update_best_costs(self, new_cost):
        self.update_costs(new_cost, new_cost)

    def update_guess_costs(self, new_cost):
        self.update_costs(self.best_costs[self.x], new_cost)

    def update_costs(self, best_cost, guess_cost):
        if self.x == COSTS_LENGTH-1:
            self.x_costs = numpy.roll(self.x_costs, -1)
            self.x_costs[-1] = self.x_costs[-2]+1
            self.best_costs = numpy.roll(self.best_costs, -1)
            if self.draw_guess:
                self.guess_costs = numpy.roll(self.guess_costs, -1)
        else:
            self.x += 1

        self.best_costs[self.x] = best_cost

        self.best_costs_line.set_xdata(self.x_costs)
        self.best_costs_line.set_ydata(self.best_costs)

        if self.draw_guess:
            self.guess_costs[self.x] = guess_cost
            self.guess_costs_line.set_xdata(self.x_costs)
            self.guess_costs_line.set_ydata(self.guess_costs)

        self.costs.relim()
        self.costs.autoscale_view()
