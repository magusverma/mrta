# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 12:44:26 2015

@author: magusverma
"""
import time
from collections import defaultdict
import resource
from heapq import heappop, heappush

def runAStar(environment, startState, heuristicFunction, weight=1):
    visited = defaultdict(lambda: [False,-1])
    heap = []

    mem = 0
    start_time = time.time()
    states_expanded = 0
    
    heappush(heap,(0,[startState,0]))
    
    while(heap):
        top = heappop(heap)
        (cost, [current_state, currentG]) = top
        
        time_spent = time.time() - start_time
        mem = max(mem, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024*1024))

        if current_state.isGoalState():
            ans = cost
            if current_state.parent is not None:
                ans += visited[current_state.parent.getRep()][1]

            print "==>", ans, states_expanded,time_spent,mem," MB" 
            return current_state

        # time check
        if time_spent > 60:
            # more than 100 secs elapsed
            print "==>",-1, states_expanded,time_spent,mem," MB TLE" 
            return current_state

        # mem check 
        if mem > 1000:
            # more than 1000 megs used
            print "==>",-1, states_expanded,time_spent,mem," MB OOM" 
            return current_state
            
        elif not visited[current_state.getRep()][0]: 
            visited[current_state.getRep()] = [True, cost]

            states_expanded += 1
            
            neighbours = current_state.getNeighbourStates()
            for neighbour in neighbours:
                g = currentG + current_state.getDistance(neighbour)
                hv = heuristicFunction(neighbour)
                print "( g = %d , h = %d ):" % (g,hv)
                if hv==0:
                    print " DONE ",neighbour.robots, neighbour.picked,g, hv
                f = g+(weight*hv)
                # neighbour.setAllocation(hdetails)
                heappush(heap,(f,[neighbour,g]))
                
    print "==> Failed in Finding a Solution, exhausted all possibilities in heap"
    return startState;