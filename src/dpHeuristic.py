# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 15:35:50 2015

@author: magusverma
"""
from bruteUtils import increment, reached_limit
from itertools import permutations
inf = 99999999999999999
#adj = [[0,15,7],[15,0,2],[7,2,0]]
n = None
dp = None 
robot_pos_list = None
target_pos_list = None
precomputed_distances = None
def tspdp(start,s):
    print start, s
    global dp
    if len(s) < 2:
        return 0
    bset = sum([1<<i for i in s])
    if dp[start][bset] != -1:
        return dp[start][bset]
    s_ = s[:]
    if start in s:
        s_.remove(start)
    
    minn = inf 
    
    for i,v in s_:
        minn = min(minn,tspdp(i, s_) + precomputed_distances[str(target_pos_list[start])][target_pos_list[]])
    dp[start] [bset]= minn
    return dp[start][bset]

print(tspdp(0,[0,1,2]))

def get_tsp_cost(robot, targets, target_pos_list, precomputed_distances, show_best = False):
    if len(targets) == 0:
        return 0
    best_cost = inf
    for c,i in enumerate(target_pos_list):
        best_cost = min(best_cost, tspdp(c, target_pos_list) + precomputed_distances[str(i)][robot[0]][robot[1]] )
   # if show_best:
    #if best_cost ==0:
    #print "For Robot at", robot, " with allocs ", targets, " best tsp order : ", best_combin, " , cost = ", best_cost
    return best_cost

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
    
def get_best_allocation_cost(allocations, robot_pos_list, target_pos_list, precomputed_distances, show_best = False):
    best_alloc_cost, best_alloc = inf, []
    for allocation in allocations:
        alloc_cost = 0
        for i, robot in enumerate(robot_pos_list):
            alloc_cost += get_tsp_cost(robot, allocation[i], target_pos_list, precomputed_distances, show_best= False)
        if alloc_cost < best_alloc_cost:
            best_alloc_cost, best_alloc = alloc_cost, allocation
    return [best_alloc_cost,best_alloc]

def bestTSPSumHeuristicDP(state):
    global robot_pos_list, precomputed_distances,n, dp, target_pos_list
    precomputed_distances = state.environment.precomputedSingleSourceDistances
    robot_pos_list = state.robots
    target_pos_list = state.getPendingTargets()
    n = len(robot_pos_list)
    dp = [[-1 for j in range(n*(2**n))] for i in range(n)]
    # precomputed_distances must be computed 
    if len(precomputed_distances.keys()) < len(target_pos_list):
        print "Precomputation of distance needs to be done for this heuristic"
        return
    allocations = get_all_allocation_combination(robot_pos_list, target_pos_list)
    return get_best_allocation_cost(allocations, robot_pos_list, target_pos_list, precomputed_distances)

