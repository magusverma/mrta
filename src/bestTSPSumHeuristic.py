# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 13:55:26 2015

@author: magusverma
"""
from bruteUtils import increment, reached_limit
from itertools import permutations
inf = 99999999999999999

def get_all_allocation_combination(robot_pos_list, target_pos_list):
    # i'th target is allocated to which value robot
    base = [0 for i in range(len(target_pos_list))]
    limit = [len(robot_pos_list) for i in range(len(target_pos_list))]
    allocations = []
    while(True):
        allocations.append([[] for i in range(len(robot_pos_list))])
        for target, robot in enumerate(base):
            allocations[-1][robot].append(target_pos_list[target])
        if reached_limit(base, limit):
            break
        increment(base, limit)
    return allocations
    
def get_tsp_cost(robot, targets, target_pos_list, precomputed_distances, show_best = False):
    if len(targets) == 0:
        return 0
    possible_visit_orders = list(permutations(targets,len(targets)))
    best_cost = inf
    best_combin = []
    for order in possible_visit_orders:
        #order_cost = precomputed_distances[str(order[0])][robot[0]][robot[1]]
        order_cost = abs(order[0][0] - robot[0]) + abs(order[0][1] - robot[1])
        #print robot, order[0], "O0=>",precomputed_distances[str(order[0])][robot[0]][robot[1]]
        for i,v in enumerate(order):
            if i!=0:
                # to go from target i-1 to target i
                #order_cost += precomputed_distances[str(order[i])][order[i-1][0]][order[i-1][1]]
                order_cost += abs(order[i][0] - order[i-1][0]) + abs(order[i][1] - order[i-1][0])
                #print order[i], order[i-1], "=>",precomputed_distances[str(order[i])][order[i-1][0]][order[i-1][1]]
        if order_cost < best_cost:
            best_cost = order_cost
            best_combin = order
   # if show_best:
    #if best_cost ==0:
    #print "For Robot at", robot, " with allocs ", targets, " best tsp order : ", best_combin, " , cost = ", best_cost
    return best_cost

def get_best_allocation_cost(allocations, robot_pos_list, target_pos_list, precomputed_distances, show_best = False):
    best_alloc_cost, best_alloc = inf, []
    for allocation in allocations:
        alloc_cost = 0
        for i, robot in enumerate(robot_pos_list):
            alloc_cost += get_tsp_cost(robot, allocation[i], target_pos_list, precomputed_distances, show_best= False)
        if alloc_cost < best_alloc_cost:
            best_alloc_cost, best_alloc = alloc_cost, allocation
    return [best_alloc_cost,best_alloc]

def bestTSPSumHeuristic(state):
    precomputed_distances = state.environment.precomputedSingleSourceDistances
    robot_pos_list = state.robots
    target_pos_list = state.getPendingTargets()
    # precomputed_distances must be computed 
    if len(precomputed_distances.keys()) < len(target_pos_list):
        print "Precomputation of distance needs to be done for this heuristic"
        return
    allocations = get_all_allocation_combination(robot_pos_list, target_pos_list)
    return get_best_allocation_cost(allocations, robot_pos_list, target_pos_list, precomputed_distances)

    