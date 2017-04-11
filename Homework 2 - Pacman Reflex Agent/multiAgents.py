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

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to add
      additional functions, so long as you don't touch the existing
      method headers.
    """

    def getAction(self, gameState):
        """
        !! Do not change this method !!

        getAction takes a GameState and returns
        some Directions.X for X in the set
        {North, South, West, East, Stop}

        getAction chooses among the best options
        according to the evaluation function --
        it is your job to improve that.
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]


    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed action
        and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)   #Generate next move
        newPos = successorGameState.getPacmanPosition() #position of pacman after move tuple(x,y)
        newFood = successorGameState.getFood()  #grid of food booleans
        newGhostStates = successorGameState.getGhostStates()    #list of ghost states
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates] #list of ghost scare times

        "*** YOUR CODE HERE ***"
        curFood = currentGameState.getFood()    #Get current food
        curGhostStates = currentGameState.getGhostStates()  #Get current ghost states
        capsuels = currentGameState.getCapsules()   #Get current capsuels
        curPos = currentGameState.getPacmanPosition()   #Get Pacman's current position
        curFoodList = curFood.asList()  #Get a list of all current food nodes
        remFood = len(curFoodList)  #Get a count of the remaining food on the board
        ghostState = curGhostStates[0]  #Get the ghost's state
        ghostPos = ghostState.configuration.getPosition()   #Get the Ghost's current position
        ghostDist = manhattanDistance(newPos, ghostPos) #Get Distance from Pacman's new position to current Ghost's position
        timer = ghostState.scaredTimer  #Store the scare timer for future use
        grade = 0   #Keeps track of total grade for this action

        """
        Christopher Potter
        3770-01
        Homework 2
        Question 3
        Average Score: 1442.6
        High Score: 1455.0

        General Logic:
            1. If the ghost is scared and there is only one food left, chase it and eat it
            2. If the ghost is scared and there are multiple food left, focus food until ghost timer is -
                - almost less than distance from pacman to ghost
            3. If Pacman clears far enough right, grab the capsuel
            4. If the ghost isnt scared, and there is only one food left, get the capsuel
            5. If the ghost isnt scared and there are multiple food focus on eating food left to right
            6. If no capsuel, eat the last food
        """
        """ Changeable Weights  """
        eatCapsuel = 1000 #1000   - Grade if move will cause pacman to eat a capsuel, adds to grade
        goToCapsuel = 100 #100  - Used to get Pacman closer to a capsuel, subtracts from grade
        huntGhost = 100 #100  - Multiplier to get pacman closer to scared ghosts, subtracts from grade
        runFromGhost = 1000 #1000 - If move would kill Pacman, subtracts from grade
        eatFood = 50 #50 - If move would have Pacman eat a food, adds to grade
        westFood = 1 #1 - If there is food west of Pacman, adds to grade
        ghostMaxWest = 15 #15 - The max distance the ghost can go left before Pacman focuses him
        ghostRangeOffset = 4 #4 - Subtracts from ghost scare timer to determine if Pacman should focus the Ghost or food
        pacmanCapsuelGrab = 20 #20 - When Pacman earches this x pos on the board he will grab the capsuel

        #Handle spoopy ghost
        if timer > 0:  #if the ghost is scared
            if remFood == 1: #If there is only one food remaining
                grade -= ghostDist*huntGhost    #Hunt the ghost double time!
            grade -= ghostDist*huntGhost    #Hunt the ghost
        else:   #if ghost is not scared
            if ghostDist <= 1:   #if this action would put a ghost on top of you
                    grade -= runFromGhost   #GET OUT OF THERE
            if ghostDist < 3:    #if the ghost is closer than 3 spaces (and not scared)
                grade -= ghostDist   #run away

        #Get those capsuels!
        if capsuels:#If capsuels exist
            if remFood == 1 or manhattanDistance(ghostPos, capsuels[0]) > ghostMaxWest or curPos[0] > pacmanCapsuelGrab:  #If there is only one food left or the ghost goes too far left or -
                for capsuel in capsuels:    #For each capsuel                                                                   - Pacman clears far enough right
                    distCap = manhattanDistance(newPos, capsuel)    #Get the distance to it
                    if distCap == 0:    #If this action would put you on a capsuel
                        grade += eatCapsuel    #EAT IT NOM NOM
                    else:   #If this action would not put you on a capsuel
                        grade -= distCap*goToCapsuel   #Use distance to gauge score, hopefully a legal move will get you closer to it

        #EAT THE FOOD
        closestFood = -5    #Placeholder for finding the closest food node
        for node in curFoodList:    #For each food node
            distFood = manhattanDistance(newPos, node)  #Find the distance from pacman to food node
            if distFood < closestFood or closestFood == -5: #If current food node is closer than closest recorded food or if default value
                closestFood = distFood  #Set closest food to the current food node
            if distFood == 0:   #If current move would eat a food node
                if capsuels and remFood == 1 or timer > 0 and remFood == 1: #If capsuels exist and there is only one food left or the ghost is scared and there is only one food left
                    grade -= eatFood*10 #DO NOT EAT THE FOOD (focus on the capsuels / ghost)
                if timer == 0  or timer > 0 and remFood > 1 and timer-ghostRangeOffset < ghostDist: #If the ghost is not scared or the ghost is scared and -
                    grade += eatFood #EAT THE FOOD NOM NOM                                            - there is more than one food and you are still within range of the ghost
            grade -= closestFood #Use distance to gauge score, a smaller value will move pacman towards food

        #Weigh food to the West as highest priority
        if action == Directions.WEST: #If the action is move West
            if countWestFood(curFoodList, newPos) == 1: #If there is food West of Pacman
                grade += countWestFood(curFoodList, newPos)*westFood  #Increase score in West direction

        return grade    #Return final score after all calculations

def countWestFood(listOfFood, pacPos):  #A function to return all food to the left of pacman
    for food in listOfFood: #For each food in the list of food
        if food[0] < pacPos[0]: #If the current food's X position is less than Pacmans X position
            return 1    #Return 1, meaning there is food West of Pacman
    return 0    #Return 0, meaning there is NO food west of Pacman
