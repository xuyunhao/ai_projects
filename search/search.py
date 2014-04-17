# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util
import searchAgents
import copy

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  "*** YOUR CODE HERE ***"
  
    #util.raiseNotDefined()
  
  fringe = []
  explored = []
  fringe.append((problem.getStartState(),'',0))
     
  return DFSRecursive(fringe, problem, explored)
  
def DFSRecursive(fringe, problem, explored):
    node = fringe.pop()    
    explored.append(node[0])
    
    if problem.isGoalState(node[0]):
        return []
    successors = problem.getSuccessors(node[0])
    if successors:
        successors.reverse()
    for i in (successors):
        if i[0] not in explored:
            fringe.append(i)
            tmpPath = DFSRecursive(fringe, problem, explored)
            if (tmpPath != None):
                tmpPath.insert(0,i[1])
                return tmpPath


def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"
  "*** YOUR CODE HERE ***"
  #util.raiseNotDefined()
  if (len(problem.getStartState()) > 1):
      problemType = problem.getStartState()[1]
      if (problemType == 'corners'):
          return BFSCorners(problem)
  node = ((problem.getStartState(),'',0),[])
  explored = []
  path = []
  fringe = []
  fringe.append(node)
  
  while (not problem.isGoalState(node[0][0])):
      
      for i in problem.getSuccessors(node[0][0]):
          if i[0] not in explored:
              tmpPath = node[1][:]
              tmpPath.append(i[1])
              fringe.append(((i), tmpPath))
      explored.append(node[0][0])

      fringe.remove(node)
      if len(fringe) == 0:
        break
      node = fringe[0]

      while node[0][0] in explored:
        fringe.remove(node)
        if len(fringe) == 0:
          break
        node = fringe[0]

  return node[1]
  

def BFSCorners(problem):
    node = [(problem.getStartState()[0],'',0),[],problem.getStartState()[2][:],[]]
    fringe = []
    fringe.append(node)
    
    while (len(node[2]) > 0):
        path = node[1]
        
        for i in problem.getSuccessors(node[0][0]):
            if i[0] not in node[3]:
                tmpPath = path[:]
                tmpPath.append(i[1])
                tmpGoals = node[2][:]
                tmpExplored = node[3][:]
                tmpExplored.append(node[0][0])
                fringe.append([(i),tmpPath,tmpGoals,tmpExplored])
        fringe.remove(node)
        
        if (problem.isGoalState(node[0][0]) and node[0][0] not in node[3]):
            node[3] = []
            node[2].remove(node[0][0])
        
        if len(fringe) == 0:
          break
        node = fringe[0]
        
    return node[1]
  
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  #util.raiseNotDefined()
  
  explored = {}
  start = problem.getStartState()
  Goal = ""
  explored[start] = ([], 0)
  orderedList = []
  succs = problem.getSuccessors(start)
  for s in succs:
      orderedList.append((s[0], s[1], s[2], start))
  orderedList = sorted(orderedList, key=lambda orderedList:(orderedList[2]))
#  print orderedList
  while not (orderedList == []):
      curr = orderedList[0]
      pred = curr[3]
      if pred not in explored:
          return []
      if problem.isGoalState(curr[0]):
          Goal = curr[0]
          cost = curr[2]
          if curr[0] not in explored:
              path = copy.deepcopy(explored[pred][0])
              path.append(curr[1])
              explored[curr[0]] = (path, cost)
              break
      else:
          if curr[0] not in explored:
              path = copy.deepcopy(explored[pred][0])
              path.append(curr[1])
              cost = curr[2]
              explored[curr[0]] = (path, cost)
              succs = problem.getSuccessors(curr[0])
              for s in succs:
                  orderedList.append((s[0], s[1], s[2]+cost, curr[0]))
          else:
              cost = curr[2]
              if explored[curr[0]][1] > cost:
                  path = copy.deepcopy(explored[pred][0])
                  path.append(curr[1])
                  explored[curr[0]] = (path, cost)

      orderedList = orderedList[1:]
      orderedList = sorted(orderedList, key=lambda orderedList:(orderedList[2]))
#      print orderedList
  return explored[Goal][0]
  

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

class Node:
  def __init__(self, state):
    self.actionList = []
    self.state = state
    self.cumulativeCost = 0

  def getState(self):
    return self.state

  def getActions(self):
    return self.actionList

  def setActionList(self, actions):
    self.actionList = actions[:]

  def addAction(self, action):
    self.actionList.append(action)

  def getDepth(self):
    return len(self.actionList)

  def getCumulativeCost(self):
    return self.cumulativeCost

  def setCumulativeCost(self, cost):
    self.cumulativeCost = cost

def makeNode(state):
    return Node(state)

def insertAllWithCostAndHeuristic(queue, nodeList, heuristic, problem):
    for node in nodeList:
        queue.push(node, node.getCumulativeCost() + heuristic(node.getState(), problem))

def expand(node, problem):
    parentNode = node
    childList = []
    #print node.getActions()
    successors = problem.getSuccessors(node.getState())
    #print successors
    for i in range(len(successors)):
      successor = successors[i]
      child = makeNode(successor[0])
      child.setActionList(parentNode.getActions())
      child.addAction(successor[1])
      child.setCumulativeCost(parentNode.getCumulativeCost() + successor[2])
      childList.append(child)

    return childList

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  closed = []
  fringe = util.PriorityQueue()
  node = makeNode(problem.getStartState())
  node.setCumulativeCost(0)
  fringe.push(node, node.getCumulativeCost() + heuristic(node.getState(), problem))

  while True:
    if fringe.isEmpty():
        return []

    node = fringe.pop()
    
    if problem.isGoalState(node.getState()):
        return node.getActions()

    if node.getState() not in closed:
        closed.append(node.getState())
        insertAllWithCostAndHeuristic(fringe, expand(node, problem), heuristic, problem)    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch