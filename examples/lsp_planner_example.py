#!/usr/bin/env python
"""A minimal example that loads an environment from a png file, runs lazy shortest path planner and returns the path. 
The search process and final path are rendered

Author: Mohak Bhardwaj
Date: 20 October, 2018

"""

import sys
sys.path.insert(0, "..")
import matplotlib.pyplot as plt
import time
from planning_python.environment_interface.env_2d import Env2D
from planning_python.state_lattices.common_lattice.xy_analytic_lattice import XYAnalyticLattice
from planning_python.cost_functions.cost_function import PathLengthNoAng, UnitCost, LazyCost
from planning_python.heuristic_functions.heuristic_function import EuclideanHeuristicNoAng, ManhattanHeuristicNoAng
from planning_python.data_structures.planning_problem import PlanningProblem
from planning_python.planners import LSPPlanner, Astar
import os


#Step1: Set some problem parameters
x_lims = [0, 201] # low(inclusive), upper(exclusive) extents of world in x-axis
y_lims = [0, 201] # low(inclusive), upper(exclusive) extents of world in y-axis
start = (10, 10)    #start state(world coordinates)
goal = (199, 199)  #goal state(world coordinates)
visualize = False

#Step 2: Load environment from file 
envfile = os.path.abspath("../../motion_planning_datasets/forest/train/259.png")
env_params = {'x_lims': x_lims, 'y_lims': y_lims}
e = Env2D()
e.initialize(envfile, env_params)

#Step 3: Create lattice to overlay on environment
lattice_params = dict()
lattice_params['x_lims']          = x_lims # Usefule to calculate number of cells in lattice 
lattice_params['y_lims']          = y_lims # Useful to calculate number of cells in lattice
lattice_params['resolution']      = [1, 1]   # Useful to calculate number of cells in lattice + conversion from discrete to continuous space and vice-versa
lattice_params['origin']          = start    # Used for conversion from discrete to continuous and vice-versa. 
lattice_params['rotation']        = 0        # Can rotate lattice with respect to world
lattice_params['connectivity']    = 'eight_connected' #Lattice connectivity (can be four or eight connected for xylattice)
lattice_params['path_resolution'] = 1         #Resolution for defining edges and doing collision checking (in meters)

l = XYAnalyticLattice(lattice_params)

#Step 4: Create cost and heuristic objects
true_cost_fn = PathLengthNoAng()                        #Penalize length of path
heuristic_fn = EuclideanHeuristicNoAng()      
lazy_cost_fn = LazyCost(PathLengthNoAng, weight=1)

#Step 5: Create a planning problem
prob_params = {'heuristic_weight': 1.0}        
start_n = l.state_to_node(start)
goal_n = l.state_to_node(goal)
prob = PlanningProblem(prob_params)
prob.initialize(e, l, true_cost_fn, heuristic_fn, start_n, goal_n, visualize=visualize)
prob.set_lazy_cost(lazy_cost_fn)

#Step 6: Create Planner object and ask it to solve the planning problem
planner = LSPPlanner()
base_planner = Astar()
planner.initialize(prob, base_planner, policy=0)
path, path_cost, num_edge_evals, plan_time, num_iters = planner.plan(max_iters=50)

print('Path: ', path)
print('Path Cost: ', path_cost)
print('Number of Expansions: ', num_edge_evals)
print('Time taken: ', plan_time)
print('Num planning iterations', num_iters)

e.initialize_plot(start, goal, grid_res=lattice_params['resolution'], plot_grid=False)
e.plot_path(path, 'solid', 'red', 3)
plt.show()
