# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 03:13:19 2015

@author: magusverma
"""

import sys
from inputUtil import getProblemInstanceFrom    
from distanceUtil import getProcomputedDistancesFor
#from bestTSPSumHeuristic import bestTSPSumHeuristic
from astarUtil import runAStar

grid, robots, targets = getProblemInstanceFrom(sys.argv[1])
# eg. [[True, False .. ], [False, True ..]] , [[x,y]...] , [[x,y]...]

'''
grid = [[True for i in range(5)] for j in range(5)]
grid[1][1] = False
grid[2][1] = False
targets = [[0,0],[2,3],[1,2],[1,4]]
'''

precomputedSingleSourceDistances = getProcomputedDistancesFor(grid, targets)
#eg. {'[x,y]': [[0,1..],[1,2..]]}

from stateDefinitions import MRTAEnvironment,MRTAState
environment = MRTAEnvironment(grid, targets)
startState = MRTAState(robots, environment)
#eg. startState.picked {'[2, 0]': [False, None], '[3, 2]': [False, None]}
#eg. startState.robots [[3, 0], [3, 1]]

#heuristicFunction = bestTSPSumHeuristic

solution = runAStar(environment, startState, lambda x: 0)