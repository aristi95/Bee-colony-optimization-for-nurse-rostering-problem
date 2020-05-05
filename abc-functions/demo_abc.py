import numpy as np
import matplotlib.pyplot as plt

from algorithm import ABC

from matplotlib.style import use

from objective_function import Rastrigin
from objective_function import Rosenbrock
from objective_function import Sphere
from objective_function import Schwefel


use('classic')


def get_objective(objective, dimension=30):
    objectives = {'Sphere': Sphere(dimension),
                  'Rastrigin': Rastrigin(dimension),
                  'Rosenbrock': Rosenbrock(dimension),
                  'Schwefel': Schwefel(dimension)}
    return objectives[objective]


def simulate(obj_function, colony_size=30, n_iter=100,
             max_trials=100, simulations=50):
    sim = range(simulations)
    values = np.zeros(n_iter)
    box_optimal = []
    result = []
    for _ in range(simulations):
        optimizer = ABC(obj_function=get_objective(obj_function),
                        colony_size=colony_size, n_iter=n_iter,
                        max_trials=max_trials)
        optimizer.optimize()
        values += np.array(optimizer.optimality_tracking)
        box_optimal.append(optimizer.optimal_solution.fitness)
        print(optimizer.optimal_solution.pos)
        values /= simulations
        result.append(values[0])

    plt.plot(sim, result, lw=0.5, label=obj_function)
    plt.legend(loc='upper right')


def main():
    
    plt.figure(figsize=(10, 7))
    simulate('Sphere')
    plt.ticklabel_format(axis='y', style='sci', scilimits=(-2, 2))
    plt.xticks(rotation=45)
    plt.show()
    """
    plt.figure(figsize=(10, 7))
    simulate('Schwefel')
    plt.ticklabel_format(axis='y', style='sci', scilimits=(-2, 2))
    plt.xticks(rotation=45)
    plt.show()
    plt.figure(figsize=(10, 7))
    simulate('Rastrigin')
    plt.ticklabel_format(axis='y', style='sci', scilimits=(-2, 2))
    plt.xticks(rotation=45)
    plt.show()
    plt.figure(figsize=(10, 7))
    simulate('Rosenbrock')
    plt.ticklabel_format(axis='y', style='sci', scilimits=(-2, 2))
    plt.xticks(rotation=45)
    plt.show()
    """

if __name__ == '__main__':
     main()
