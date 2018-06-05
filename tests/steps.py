from tests import modifications
import time
import matplotlib.pyplot as plt

'''
        Test for steps.
        
        This code will run bc - algorithm for statistics.
        
        Graphical interpretation: each step represents x, each time value - y

'''


class StepsTest:

    def __init__(self, scouts, best_amount, workers, steps=500):
        self.best_amount = best_amount
        self.steps = steps
        self.bca = modifications.BCA('Steps testing', 'settings.txt')
        self.scouts = scouts
        self.workers = workers
        self.complexity = {}

    def start(self):
        for iterations in range(self.steps):
            then = float(time.clock())
            self.bca.bca(iterations, self.scouts, self.workers, self.best_amount)
            now = float(time.clock())
            self.complexity[iterations] = now - then

    def show_graphical_result(self):
        plt.plot(self.complexity.keys(), self.complexity.values())
        plt.show()


steps = int(input('Enter steps amount: '))
best_amount = int(input('Enter amount of best solutions: '))
scouts = int(input('Enter scouts amount: '))
workers = int(input('Enter workers amount: '))
test = StepsTest(scouts, best_amount, workers, steps)
test.start()
test.show_graphical_result()
