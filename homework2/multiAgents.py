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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
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
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** BEGIN YOUR CODE HERE ***"

        foodScoreComponent = 0
        distancesToFood = [util.manhattanDistance(newPos, food) for food in newFood.asList()]
        if distancesToFood:
            closestFoodDist = min(distancesToFood)
            foodScoreComponent = 10.0 / closestFoodDist

        ghostScoreComponent = 0
        activeGhostsDistances = [util.manhattanDistance(newPos, ghost.getPosition()) for ghost, timer in zip(newGhostStates, newScaredTimes) if timer == 0]
        scaredGhostsCount = sum(1 for timer in newScaredTimes if timer > 0)
        if activeGhostsDistances:
            closestGhostDist = min(activeGhostsDistances)
            if closestGhostDist > 0:
                ghostScoreComponent = -50.0 / closestGhostDist

        foodLeftPenalty = -2 * len(newFood.asList())

        modifiedScore = successorGameState.getScore() + foodScoreComponent + ghostScoreComponent + foodLeftPenalty

        if action == Directions.STOP:
            modifiedScore -= 20.0

        return modifiedScore
        "*** END YOUR CODE HERE ***"
        # ^^^ you should return something in the above block
        
        # but by default, this is the evaluation function before you put your code in
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** BEGIN YOUR CODE HERE ***"
        # util.raiseNotDefined()

        # def maxValue(gameState):
        #     v = -1000000000000
        #     for action in gameState.getLegalActions(0):
        #         v = max(v, minValue(successorGameState))
        #     return v

        # def minValue(state):
        #     v = 10000000000000
        #     for action in gameState.getLegalActions(ghost):
        #         v = min(v, maxValue(successorGameState))
        #     return v

        # if GameState.isWin(): 
        #     return maxValue()
        # if GameState.isLose(): 
        #     return minValue(state)

        # self.evaluationFunction = leaves

        def minimax(agentIndex, depth, gameState):
            if gameState.isWin() or gameState.isLose() or depth == self.depth * gameState.getNumAgents():
                return self.evaluationFunction(gameState)

            if agentIndex == 0:
                return max_value(gameState, depth)[0]

            else:
                return min_value(gameState, agentIndex, depth)[0]

        def max_value(gameState, depth):
            best_score = -9999999999999999999999999999
            best_action = None
            for action in gameState.getLegalActions(0):  
                if action == Directions.STOP: 
                    continue
                successor = gameState.generateSuccessor(0, action)
                score = minimax(1, depth + 1, successor)
                if score > best_score:
                    best_score = score
                    best_action = action
            return best_score, best_action

        def min_value(gameState, agentIndex, depth):
            best_score = 9999999999999999999999999999
            best_action = None
            for action in gameState.getLegalActions(agentIndex):
                successor = gameState.generateSuccessor(agentIndex, action)
                next_agent = (agentIndex + 1) % gameState.getNumAgents()
                score = minimax(next_agent, depth + 1, successor)
                if score < best_score:
                    best_score = score
                    best_action = action
            return best_score, best_action

        _, action = max_value(gameState, 0)
        return action
        "*** END YOUR CODE HERE ***"

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** BEGIN YOUR CODE HERE ***"
        # util.raiseNotDefined()

        def max_value(gameState, depth, alpha, beta):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState), None
            v =  -9999999999999999999999999999
            best_action = None
            for action in gameState.getLegalActions(0):
                if action == Directions.STOP:
                    continue
                successor = gameState.generateSuccessor(0, action)
                score = min_value(successor, depth, 1, alpha, beta)[0] 
                if score > v:
                    v, best_action = score, action
                if v > beta:
                    return v, best_action
                alpha = max(alpha, v)
            return v, best_action

        def min_value(gameState, depth, agentIndex, alpha, beta):
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState), None
            v = 9999999999999999999999999999
            best_action = None
            for action in gameState.getLegalActions(agentIndex):
                successor = gameState.generateSuccessor(agentIndex, action)
                if agentIndex == gameState.getNumAgents() - 1:  
                    score = max_value(successor, depth + 1, alpha, beta)[0] 
                else:
                    score = min_value(successor, depth, agentIndex + 1, alpha, beta)[0]
                if score < v:
                    v, best_action = score, action
                if v < alpha:
                    return v, best_action
                beta = min(beta, v)
            return v, best_action

        _, action = max_value(gameState, 0, -9999999999999999999999999999, 9999999999999999999999999999)
        return action
        "*** END YOUR CODE HERE ***"

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** BEGIN YOUR CODE HERE ***"
        # util.raiseNotDefined()
        def expectimax(agentIndex, depth, gameState):
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            
            if agentIndex == 0:  
                if depth == self.depth: 
                    return self.evaluationFunction(gameState)
                return max_value(gameState, depth)
            else: 
                return exp_value(gameState, agentIndex, depth)

        def max_value(gameState, depth):
            v = -999999999999999999999999999999999
            best_action = Directions.STOP
            for action in gameState.getLegalActions(0):
                successor = gameState.generateSuccessor(0, action)
                score = expectimax(1, depth, successor)
                if score > v:
                    v, best_action = score, action
            return v if depth != 0 else best_action

        def exp_value(gameState, agentIndex, depth):
            v = 0
            actions = gameState.getLegalActions(agentIndex)
            if not actions:
                return self.evaluationFunction(gameState)
            prob = 1.0 / len(actions)
            for action in actions:
                successor = gameState.generateSuccessor(agentIndex, action)
                next_agent = agentIndex + 1
                if next_agent >= gameState.getNumAgents(): 
                    next_agent = 0
                    next_depth = depth + 1
                else:
                    next_depth = depth
                v += prob * expectimax(next_agent, next_depth, successor)
            return v

        return expectimax(0, 0, gameState)
        "*** END YOUR CODE HERE ***"

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** BEGIN YOUR CODE HERE ***"
    # util.raiseNotDefined()
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    score = currentGameState.getScore()

    foodDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]
    if foodDistances:
        score += 1.0 / min(foodDistances)

    score -= 3 * len(foodDistances)

    capsules = currentGameState.getCapsules()
    score -= 20 * len(capsules)

    ghostDistances = [manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates if ghost.scaredTimer == 0]
    scaredGhosts = [manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates if ghost.scaredTimer > 0]

    if ghostDistances:
        minGhostDistance = min(ghostDistances)
        if minGhostDistance > 0:
            score -= 2.0 / minGhostDistance

    if scaredGhosts:
        score += 10 * sum([1.0 / (dist + 1) for dist in scaredGhosts])

    return score
    "*** END YOUR CODE HERE ***"

better = betterEvaluationFunction