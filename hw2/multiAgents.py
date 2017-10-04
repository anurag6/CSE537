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
from game import Actions

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        """print ("******New set of posns******")
        print ("current pos:",gameState.getPacmanPosition())
        print ("Legal neighbours:", Actions.getLegalNeighbors(gameState.getPacmanPosition(),gameState.getWalls()))"""
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        #print("best scores available:",bestScore)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        #print ("Action taken:",legalMoves[chosenIndex])
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood().asList()
        if successorGameState.getNumFood() > 0:
            minFoodDistance = min([manhattanDistance(newPos,pos) for pos in newFood])
        else:
            minFoodDistance = 0
        """print("***")
        print ("New food:",newFood)
        print ("newPos:", newPos)
        print ("minFoodDistance:",minFoodDistance)
        print ("successor has food:", successorGameState.hasFood(newPos[0],newPos[1]))
        print ("current has food", currentGameState.hasFood(newPos[0],newPos[1]))"""
        newGhostStates = successorGameState.getGhostStates()
        newGhostPositions = nextPossibleGhostStates(currentGameState)
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        score = successorGameState.getScore()
        if newPos in newGhostPositions:
            score -= 400
        if currentGameState.hasFood(newPos[0],newPos[1]):
            score += 50
        score -= minFoodDistance
        return score

def nextPossibleGhostStates(currentGameState):
    result = []
    for index in range(1,currentGameState.getNumAgents()):
        ghostState = currentGameState.data.agentStates[index]
        if ghostState.scaredTimer > 0:
            continue
        validPositions=Actions.getLegalNeighbors(ghostState.getPosition(),currentGameState.getWalls())
        result.extend(validPositions)
    return result

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
        successors = self.getSuccessorsWithValuesAction(gameState,0,0)
        value = max(successors,key=lambda s: s[0])
        return value[1]

    def getSuccessorsWithValuesAction(self, gameState, agentId, currDepth):
        #print("\n***getSuccessorsWithValuesAction***")
        #print ("agentId:",agentId,"currDepth:", currDepth,"target depth:",self.depth)
        if agentId == 0:
         #   print ("pacman")
            currDepth+=1
        legalMoves = gameState.getLegalActions(agentId)
        if (agentId == gameState.getNumAgents()-1) and (currDepth == self.depth):   #if it is the last agent for given depth, dont evaluate expand xuccessors, jsut get scores.
            successorsValues = [(self.evaluationFunction(gameState.generateSuccessor(agentId,action)),action) for action in legalMoves]
        else:
            successors = [[gameState.generateSuccessor(agentId,action),action] for action in legalMoves]
          #  print ("Successors:",successors)
            successorsValues = []
            for successor in successors:
           #     print ("Successor:",successor)
                if successor[0].isWin() or successor[0].isLose():   #is a leaf node
            #        print ("Is a leaf node")
                    value = self.evaluationFunction(successor[0])
                else:
                    if (agentId+1)%successor[0].getNumAgents() == 0:
             #           print ("Picking max value")
                        value = max(self.getSuccessorsWithValuesAction(successor[0],(agentId+1)%successor[0].getNumAgents(),currDepth),key=lambda s: s[0])[0]
                    else:
              #          print ("Picking min value")
                        value = min(self.getSuccessorsWithValuesAction(successor[0],(agentId+1)%successor[0].getNumAgents(),currDepth),key=lambda s: s[0])[0]
                successorsValues.append((value,successor[1]))
        #print ("successorsValues",successorsValues)
        return successorsValues

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        successors = self.getSuccessorsWithValuesAction(gameState, 0, 0,float("-inf"),float("inf"))
        value = max(successors, key=lambda s: s[0])
        return value[1]

    def getSuccessorsWithValuesAction(self, gameState, agentId, currDepth,alpha,beta):
        #print("\n***getSuccessorsWithValuesAction***")
        #print ("agentId:",agentId,"currDepth:", currDepth,"target depth:",self.depth,"alpha:",alpha,"beta:",beta)
        if agentId == 0:
            #print ("pacman")
            currDepth+=1
        legalMoves = gameState.getLegalActions(agentId)
        if (agentId == gameState.getNumAgents()-1) and (currDepth == self.depth):   #if it is the last agent for given depth, dont evaluate expand xuccessors, jsut get scores.
            successorsValues = []
            for action in legalMoves:
                value = (self.evaluationFunction(gameState.generateSuccessor(agentId,action)))
                successorsValues.append((value,action))
                if value < beta:
                    beta = value
                if alpha > beta:
                    break

        else:
            #print ("Successors:",successors)
            successorsValues = []
            for index,action in enumerate(legalMoves):
                successor = [gameState.generateSuccessor(agentId,action),action]
                #print ("Successor:",successor,"currdepth:",currDepth,"index:",index)
                if successor[0].isWin() or successor[0].isLose():   #is a leaf node
                    #print ("Is a leaf node")
                    value = self.evaluationFunction(successor[0])
                    if (agentId) % successor[0].getNumAgents() == 0:
                        if value > alpha:
                            alpha = value
                    else:
                        if value < beta:
                            beta = value
                else:
                    if (agentId+1)%successor[0].getNumAgents() == 0:
                        #print ("next agent is max")
                        value = max(self.getSuccessorsWithValuesAction(successor[0],(agentId+1)%successor[0].getNumAgents(),currDepth,alpha,beta),key=lambda s: s[0])[0]
                        #print ("Got value for max:",value)
                        #if value < beta:
                        #    beta = value
                    else:
                        #print ("nextagent is min")
                        value = min(self.getSuccessorsWithValuesAction(successor[0],(agentId+1)%successor[0].getNumAgents(),currDepth,alpha,beta),key=lambda s: s[0])[0]
                        #print("Got value for min:",value)
                        #if value > alpha:
                        #    alpha = value
                    if (agentId) % successor[0].getNumAgents() == 0:
                        if value > alpha:
                            alpha = value
                    else:
                        if value < beta:
                            beta = value
                successorsValues.append((value,successor[1]))
                #print ("For currdepth:",currDepth,"index:",index,"alpha:",alpha,"beta:",beta,"value:",value)
                if alpha > beta:
                 #   print ("pruning")
                    break
        #print ("successorsValues",successorsValues)
        #print ("***end***\n")
        return successorsValues

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
        successors = self.getSuccessorsWithValuesAction(gameState, 0, 0)
        value = max(successors, key=lambda s: s[0])
        return value[1]

    def getSuccessorsWithValuesAction(self, gameState, agentId, currDepth):
        #print("\n***getSuccessorsWithValuesAction***")
        #print ("agentId:",agentId,"currDepth:", currDepth,"target depth:",self.depth)
        if agentId == 0:
         #   print ("pacman")
            currDepth+=1
        legalMoves = gameState.getLegalActions(agentId)
        if (agentId == gameState.getNumAgents()-1) and (currDepth == self.depth):   #if it is the last agent for given depth, dont evaluate expand xuccessors, jsut get scores.
            successorsValues = [(self.evaluationFunction(gameState.generateSuccessor(agentId,action)),action) for action in legalMoves]
        else:
            successors = [[gameState.generateSuccessor(agentId,action),action] for action in legalMoves]
          #  print ("Successors:",successors)
            successorsValues = []
            for successor in successors:
           #     print ("Successor:",successor)
                if successor[0].isWin() or successor[0].isLose():   #is a leaf node
            #        print ("Is a leaf node")
                    value = self.evaluationFunction(successor[0])
                else:
                    if (agentId+1)%successor[0].getNumAgents() == 0:
             #           print ("Picking max value")
                        value = max(self.getSuccessorsWithValuesAction(successor[0],(agentId+1)%successor[0].getNumAgents(),currDepth),key=lambda s: s[0])[0]
                    else:
              #          print ("Picking min value")
                        value = mean([suc[0] for suc in self.getSuccessorsWithValuesAction(successor[0],(agentId+1)%successor[0].getNumAgents(),currDepth)])
                successorsValues.append((value,successor[1]))
        #print ("successorsValues",successorsValues)
        return successorsValues

def mean(iter):
    return float(sum(iter))/max(len(iter),1)

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    #successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood().asList()
    if currentGameState.getNumFood() > 0:
        minFoodDistance = min([manhattanDistance(newPos, pos) for pos in newFood])
    else:
        minFoodDistance = 0
    """print("***")
    print ("New food:",newFood)
    print ("newPos:", newPos)
    print ("minFoodDistance:",minFoodDistance)
    print ("successor has food:", successorGameState.hasFood(newPos[0],newPos[1]))
    print ("current has food", currentGameState.hasFood(newPos[0],newPos[1]))"""
    newGhostStates = currentGameState.getGhostStates()
    newGhostPositions = nextPossibleGhostStates(currentGameState)
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    "*** YOUR CODE HERE ***"
    score = currentGameState.getScore()
    if newPos in newGhostPositions:
        score -= 400
    if currentGameState.hasFood(newPos[0], newPos[1]):
        score += 50
    score -= minFoodDistance
    return score

# Abbreviation
better = betterEvaluationFunction

