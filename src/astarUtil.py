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

            print "==> solution cost = ",currentG, " , states expanded = ",states_expanded, ", time spent = ",round(time_spent,2)," secs , memory taken = ",mem,"MB" 
            return current_state

        # time check
        if time_spent > 5:
            # more than 100 secs elapsed
            print "==> solution cost = ",-1, " , states expanded = ",states_expanded, ", time spent = ",round(time_spent,2)," secs , memory taken = ",mem,"MB","TLE" 
            return current_state

        # mem check 
        if mem > 1000:
            # more than 1000 megs used
            print "==> solution cost = ",-1, " , states expanded = ",states_expanded, ", time spent = ",round(time_spent,2)," secs , memory taken = ",mem,"MB","OOM" 
            return current_state
            
        elif not visited[current_state.getRep()][0]: 
            visited[current_state.getRep()] = [True, cost]
            print " Visiting ( f = %d , g = %d , h = %d ) state=%s" % (cost, currentG, cost-currentG,current_state.getRep())
            states_expanded += 1
            
            neighbours = current_state.getNeighbourStates()
            for neighbour in neighbours:
                if not visited[neighbour.getRep()][0]:
                    g = currentG + current_state.getDistance(neighbour)
                    hv,hinfo = heuristicFunction(neighbour)
                    #if hv==0:
                    #    print " DONE ",neighbour.robots, neighbour.picked,g, hv
                    f = g+(weight*hv)
                    neighbour.setAllocation(hinfo)
                    heappush(heap,(f,[neighbour,g]))
                
    print "==> Failed in Finding a Solution, exhausted all possibilities in heap"
    return startState;

def getSolutionSteps(goalState):
    soln = [goalState]
    while(soln[-1] != None):
        soln.append(soln[-1].parent)
    return soln[::-1][1:]

def allocationChangeReport(solutionSteps):
    print "Allocation Change Report"
    init = None
    for state in solutionSteps:
        print state.getRep(),
        if init is None:
            init = state.alloc
            print state.alloc,
        else:
            flag = False
            for r in range(len(init)):
                for t in state.alloc[r]:
                    if t not in init[r]:
                        flag = True
            if flag:
                print "==> allocation changed to", state.alloc,
        print
