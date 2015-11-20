# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 03:13:19 2015

@author: magusverma
"""

import sys
#sys.stdout = open('../random_grid_results/'+sys.argv[1], 'w')
from inputUtil import getProblemInstanceFrom    
from distanceUtil import getProcomputedDistancesFor
from bestTSPSumHeuristic import bestTSPSumHeuristic
from astarUtil import runAStar, getSolutionSteps, allocationChangeReport

# Reading the input test case from filename passed in command line parameter
grid, robots, targets = getProblemInstanceFrom(sys.argv[1])
# eg. [[True, False .. ], [False, True ..]] , [[x,y]...] , [[x,y]...]

precomputedSingleSourceDistances = getProcomputedDistancesFor(grid, targets)
#eg. {'[x,y]': [[0,1..],[1,2..]]}

from stateDefinitions import MRTAEnvironment,MRTAState
environment = MRTAEnvironment(grid, targets, precomputedSingleSourceDistances)
startState = MRTAState(robots, environment)
#eg. startState.picked {'[2, 0]': [False, None], '[3, 2]': [False, None]}
#eg. startState.robots [[3, 0], [3, 1]]

heuristicFunction = bestTSPSumHeuristic
noHeuristic = lambda x: 0

goalState = runAStar(environment, startState, bestTSPSumHeuristic, weight=10)
solution = getSolutionSteps(goalState)

print 
print "targets => %s" % goalState.picked.keys()
print "solution:"
for state in solution:
    print state.getRep()

print    
allocationChangeReport(solution)

