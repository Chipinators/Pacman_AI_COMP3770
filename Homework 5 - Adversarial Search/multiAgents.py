# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        self.agents = gameState.getNumAgents()  # Used to reset the index

        """
        value()
        Inputs:
        state - the current game state
        depth - the current depth of the search
        index - the current agent being looked at

        Logic:
        - if the index value is the same as the number of agent,
            reset the index to 0 and subtract 1 from the depth to signify a new partially
        - if the state is a terminal state or the depth limit has been reached,
            return the evaluation function of the state with a None for consistency
        - if the index value is 0,
            this represents the state as Pacman's and return the maxValue function
        - if the index value is greater than 0,
            this represents any number of ghosts and return the minValue function for the current index
        """
        def value(state, depth, index):
            if index >= (self.agents):
                index = 0
                depth -= 1
            if state.isWin() or state.isLose() or depth == 0:
                return (self.evaluationFunction(state), None)
            if index == 0: # Pacman
                return maxValue(state, depth, index)
            if index > 0:  # Ghost
                return minValue(state, depth, index)

        """
        maxValue()
        Inputs:
        state - the current game state
        depth - the current depth of the search
        index - the current agent being looked at

        Logic:
        - initialize a default maxV to negative infinity and None for consistency
        - for each action the agent can take, get the value of the successor,
            pass in the current index + 1 to represent the next agent
        - if the value of the action is greater than the current maxV
            set maxV to the current score and action
        """
        def maxValue(state, depth, index):
            maxV = (float('-inf'), None)
            for action in state.getLegalActions(index):
                cur = value(state.generateSuccessor(index, action), depth, index+1)
                if cur[0] > maxV[0]:
                    maxV = (cur[0], action)
            return maxV

        """
        minValue()
        Inputs:
        state - the current game state
        depth - the current depth of the search
        index - the current agent being looked at

        Logic:
        - initialize a default minV to positive infinity and None for consistency
        - for each action the agent can take, get the value of the successor,
            pass in the current index + 1 to represent the next agent
        - if the value of the action is less than the current minV
            set minV to the current score and action
        """
        def minValue(state, depth, index):
            minV = (float('+inf'), None)
            for action in state.getLegalActions(index):
                cur = value(state.generateSuccessor(index, action), depth, index+1)
                if cur[0] < minV[0]:
                    minV = (cur[0], action)
            return minV

        return value(gameState, self.depth, 0)[1]
        util.raiseNotDefined()



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        self.agents = gameState.getNumAgents()  # Used to reset the index

        """
        value()
        Inputs:
        state - the current game state
        depth - the current depth of the search
        index - the current agent being looked at
        alpha - the current best max value
        beta  - the current best min value

        Logic:
        - if the index value is the same as the number of agent,
            reset the index to 0 and subtract 1 from the depth to signify a new partially
        - if the state is a terminal state or the depth limit has been reached,
            return the evaluation function of the state with a None for consistency
        - if the index value is 0,
            this represents the state as Pacman's and return the maxValue function
        - if the index value is greater than 0,
            this represents any number of ghosts and return the minValue function for the current index

        """
        def value(state, depth, index, alpha, beta):
            if index >= (self.agents):
                index = 0
                depth -= 1
            if state.isWin() or state.isLose() or depth == 0:
                return (self.evaluationFunction(state), None)
            if index == 0: # Pacman
                return maxValue(state, depth, index, alpha, beta)
            if index > 0:  # Ghost
                return minValue(state, depth, index, alpha, beta)

        """
        maxValue()
        Inputs:
        state - the current game state
        depth - the current depth of the search
        index - the current agent being looked at
        alpha - the current best max value
        beta  - the current best min value

        Logic:
        - initialize a default maxV to negative infinity and None for consistency
        - for each action the agent can take, get the value of the successor,
            pass in the current index + 1 to represent the next agent
        - if the value of the action is greater than the current maxV
            set maxV to the current score and action
        - if maxV is greater than beta, return maxV
        - set alpha to the max of the current alpha and maxV
        """
        def maxValue(state, depth, index, alpha, beta):
            maxV = (float('-inf'), None)
            for action in state.getLegalActions(index):
                cur = value(state.generateSuccessor(index, action), depth, index+1, alpha, beta)
                if cur[0] > maxV[0]:
                    maxV = (cur[0], action)
                if maxV[0] > beta:
                    return maxV
                alpha = max(alpha, maxV[0])
            return maxV

        """
        minValue()
        Inputs:
        state - the current game state
        depth - the current depth of the search
        index - the current agent being looked at
        alpha - the current best max value
        beta  - the current best min value

        Logic:
        - initialize a default minV to positive infinity and None for consistency
        - for each action the agent can take, get the value of the successor,
            pass in the current index + 1 to represent the next agent
        - if the value of the action is less than the current minV
            set minV to the current score and action
        - if minV is less than alpha, return minV
        - set beta to the min of the current beta and minV
        """
        def minValue(state, depth, index, alpha, beta):
            minV = (float('+inf'), None)
            for action in state.getLegalActions(index):
                cur = value(state.generateSuccessor(index, action), depth, index+1, alpha, beta)
                if cur[0] < minV[0]:
                    minV = (cur[0], action)
                if minV[0] < alpha:
                    return minV
                beta = min(beta, minV[0])
            return minV

        return value(gameState, self.depth, 0, float('-inf'), float('inf'))[1]
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        self.agents = gameState.getNumAgents() #Used to reset the index

        """
        value()
        Inputs:
        state - the current game state
        depth - the current depth of the search
        index - the current agent being looked at

        Logic:
        - if the index value is the same as the number of agent,
            reset the index to 0 and subtract 1 from the depth to signify a new partially
        - if the state is a terminal state or the depth limit has been reached,
            return the evaluation function of the state with a None for consistency
        - if the index value is 0,
            this represents the state as Pacman's and return the maxValue function
        - if the index value is greater than 0,
            this represents any number of ghosts and return the minValue function for the current index

        """
        def value(state, depth, index):
            if index >= (self.agents):
                index = 0
                depth -= 1
            if state.isWin() or state.isLose() or depth == 0:
                return (self.evaluationFunction(state), None)
            if index == 0: # Pacman
                return maxValue(state, depth, index)
            if index > 0:  # Ghost
                return expValue(state, depth, index)

        """
        maxValue()
        Inputs:
        state - the current game state
        depth - the current depth of the search
        index - the current agent being looked at

        Logic:
        - initialize a default maxV to negative infinity and None for consistency
        - for each action the agent can take, get the value of the successor,
            pass in the current index + 1 to represent the next agent
        - if the value of the action is greater than the current maxV
            set maxV to the current score and action
        """
        def maxValue(state, depth, index):
            maxV = (float('-inf'), None)
            for action in state.getLegalActions(index):
                cur = value(state.generateSuccessor(index, action), depth, index+1)
                if cur[0] > maxV[0]:
                    maxV = (cur[0], action)
            return maxV

        """
        expValue()
        Inputs:
        state - the current game state
        depth - the current depth of the search
        index - the current agent being looked at

        Logic:
        - initialize a default expV to zero and None for consistency
        - get a list of the legal actions
        - compute the uniform probability by doing 1 divided by the number of actions
        - for each action,
            add the current expV to the probability * value function of the next index
        """
        def expValue(state, depth, index):
            expV = (0, None)
            actions = state.getLegalActions(index)
            p = 1.0 / len(actions)
            for action in actions:
                expV = (expV[0] + (p * value(state.generateSuccessor(index, action), depth, index+1)[0]), action)
            return expV

        return value(gameState, self.depth, 0)[1]
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    """ GAME STATE VARIABLES """
    grade = currentGameState.getScore()             # Initialize grade to the score of the state
    ghosts = currentGameState.getGhostStates()      # Get the list of ghost states
    pacPos = currentGameState.getPacmanPosition()   # Get Pacman's current position
    caps = currentGameState.getCapsules()           # Get the list of capsuel locations
    foodList = currentGameState.getFood().asList()

    # For each ghost
    # Add the reciprocal of the distance to that ghost to the grade
    for ghost in ghosts:
        try: grade += (1/ util.manhattanDistance(pacPos, ghost.configuration.getPosition()))
        except ZeroDivisionError: continue

    # For each capsule
    # Add the reciprocal of the distance to that capsule to the grade
    for cap in caps:
            grade += (1/ util.manhattanDistance(pacPos, cap))

    return grade
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
