# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def graphSearch(problem, frontier):
    """
    Once your DFS, BFS, UCS, and A* algorithms work, unify them
    into a single, iterative graphSearch algorithm that
    requires only an object to manage the fringe.
    """
    "*** YOUR CODE HERE ***"
    closed = set()                                                  # Create the closed list
    closed.add(problem.getStartState()[0])                          # Add the first node because we "skip" it
    for succ in problem.getSuccessors(problem.getStartState()):     # For each succesor node
        frontier.push((succ, []))                                   # Add it to the frontier along with an empty list to track the path and a path cost
    while True:                                                     # While true
        if frontier.isEmpty():                                      # If frontier is empty
            return []                                               # Return empty list representing no path
        node = frontier.pop()                                       # Get one of the nodes from the frontier
        if problem.isGoalState(node[0][0]):                         # If the node is the goal state
            node[1].append(node[0][1])                              # Add that nodes direction to the list of directions
            return node[1]                                          # Return the list of directions
        if node[0][0] not in closed:                                # If the current node is not in the closed list
            closed.add(node[0][0])                                  # Add the nodes coordinates to the closed list
            for succ in problem.getSuccessors(node[0][0]):          # Get the successor states for the current node, for each successor
                frontier.push(((succ[0], succ[1], succ[2] + node[0][2]), node[1] + [node[0][1]]))   # Add it to the frontier and add it to the paths history list

    # node[0] = current state
    # node[0][0] = current position
    # node[0][1] = current direction
    # node[0][2] = current total path cost
    # node[1] = directions of current path

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    return graphSearch(problem,util.Stack())

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    return graphSearch(problem,util.Queue())

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    def priFunction(item):
        return item[0][2]

    return graphSearch(problem,util.PriorityQueueWithFunction(priFunction))

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    def priFunction(node):
        score = node[0][2] + heuristic(node[0][0], problem)
        return score

    return graphSearch(problem,util.PriorityQueueWithFunction(priFunction))


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
ucs = uniformCostSearch
astar = aStarSearch
