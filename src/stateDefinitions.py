# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 04:07:30 2015

@author: magusverma
"""

from bruteUtils import increment, reached_limit
from math import sqrt

connectedness = 5

class MRTAEnvironment:
    def __init__(self, grid, targets, precomputedSingleSourceDistances=None):
        self.grid = grid
        self.targets = targets
        self.precomputedSingleSourceDistances = precomputedSingleSourceDistances
        self.height = len(grid)
        self.width = len(grid[0])
        
class MRTAState:
    def __init__(self, robots__, environment__, picked__=None,parent__=None):
        #print "robots__ = %s, environment__ = %s, picked__= %s,parent__= %s" % ( str(robots__), str(environment__), str(picked__),str(parent__))
        self.robots = robots__
        self.environment = environment__

        # Example : {'[4, 5]': [False, None], '[6, 7]': [True, None]}
        if picked__ is None:
            self.picked = {str(i): [False,None] for i in self.environment.targets}
            for i, robot in enumerate(self.robots):
                if str(robot) in self.picked.keys():
                    self.picked[str(robot)] = [True, i]
        else:
            self.picked = picked__
        
        self.parent = parent__
        self.alloc = None
    
    def setAllocation(self,alloc):
        self.alloc = alloc
        
    def getPendingTargets(self):
        pending = []
        for target in self.environment.targets:
            if not self.picked[str(target)][0]:
                pending.append(target)
        return pending
            
    def isValidState(self):
        robos = [str(i) for i in self.robots]
        if len(robos) != len(set(robos)):
            #two robots on same grid cell
            return False
            
        for robo in self.robots:
            if (not(0<=robo[0]<self.environment.height)) or (not(0<=robo[1]<self.environment.width)):
                #outside grid
                return False
            if not self.environment.grid[robo[0]][robo[1]]:
                # robot standing on a blocked cell
                return False
                
        return True
    
    def isGoalState(self):
        return reduce(lambda x, y: x and y, [k[0] for k in self.picked.values()])
        
    def transition(self, action):
        global connectedness
        
        move_map = {}
        if connectedness == 5:
            move_map[0] = [-1,0]
            move_map[1] = [0,-1]
            move_map[2] = [0,0]
            move_map[3] = [0,1]
            move_map[4] = [1,0]
            
        robots_ = [[j for j in i] for i in self.robots]
        picked_ = self.picked.copy()
        parent_ = self
        
        # move robots to new grid cells as per actions
        for i,move in enumerate(action):
            robots_[i][0] = robots_[i][0] + move_map[move][0]
            robots_[i][1] = robots_[i][1] + move_map[move][1]
        
        #print robots_, self.robots
        # pick newly found targets
        for i,robo in enumerate(robots_):
            if str(robo) in picked_.keys() and not picked_[str(robo)][0] :
                picked_[str(robo)] = [True,i]
        
        s_ = MRTAState(robots_,self.environment,picked_,parent_) 
        
        #print "R:",s_.robots,self.robots
        
        return s_
                
    def getNeighbourStates(self):
        global connectedness
        
        neighbours = []
        
        moveCombinations = []
        
        base = [0 for i in range(len(self.robots))]
        limit = [connectedness for i in range(len(self.robots))]
        while(True):
            moveCombinations.append(base[:])
            if reached_limit(base, limit):
                break
            increment(base, limit)
            
        for move in moveCombinations:
            state = self.transition(move)
            if state.isValidState():
                neighbours.append(state)
        
        return neighbours
    
    def getDistance(self, other):
        distance = 0
        for i in range(len(self.robots)):
            for j in range(len(self.robots[i])):
                distance += sqrt(pow(self.robots[i][j] - other.robots[i][j],2))
        return distance
        
    def getRep(self):
        rep = ""
        for i in self.robots:
            rep += str(i)
        for i in self.picked.values():
            rep += str(i[0])[0]
        return rep
