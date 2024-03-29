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

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}

        Chon huong di tot nhat de di
        Lay vao getstate va tra ve huong
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state,
        ----- the remaining food (newFood)
        ----- Pacman position after moving (newPos).
        ----- newScaredTimes holds the number of moves that each ghost will remain scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        curPos = currentGameState.getPacmanPosition()
        newFoodPos = newFood.asList()
        ghostPos = successorGameState.getGhostPositions()
        ghostDis = []

        # Tinh khoang cach pacman voi ghost
        for ghost in ghostPos:
            ghostDis.append(manhattanDistance(newPos, ghost))

        # tinh evaluation
        # Khong duoc cham vao ghost
        for idx, dist in enumerate(ghostDis):
            if dist < 2 and newScaredTimes[idx] < 10:
                return (-(float("inf")))
        # Chien thang
        if len(newFoodPos) == 0:
            return float("inf")
        evaluation = 0
        # An food ngay khi co the
        if newPos in currentGameState.getFood().asList():
            evaluation = 10000
        # Neu khong gian duoc so luong food -> tim duuong den food
        else:
            if action == 'Stop':
                return (-(float("inf")))
            target = currentGameState.getFood().asList()[0]
            target_X = int(target[0])
            target_Y = int(target[1])
            curPos_X = int(curPos[0])
            curPos_Y = int(curPos[1])
            if (target_X < curPos_X) and action == 'West': evaluation += 5000
            if (target_X > curPos_X) and action == 'East': evaluation += 5000
            if (target_Y < curPos_Y) and action == 'South': evaluation += 1000
            if (target_Y > curPos_Y) and action == 'North': evaluation += 1000
        return evaluation


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
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

        -----gameState.getLegalActions(agentIndex):
                            Returns a list of legal actions for an agent
                            agentIndex=0 means Pacman, ghosts are >= 1
        -----gameState.generateSuccessor(agentIndex, action):
                            Returns the successor game state after an agent takes an action

        -----gameState.getNumAgents():
                            Returns the total number of agents in the game

        -----gameState.isWin():
                            Returns whether or not the game state is a winning state

        -----gameState.isLose():
                            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        ##Toi da hoa gia tri cho pacman
        def maxValue(gameState, depth):
            pacmanAct = gameState.getLegalActions(0)

            # Neu khong con duong di hoac thang hoac thua hoac dat den do sau can thiet thi return
            if len(pacmanAct) == 0 or gameState.isWin() or gameState.isLose() or depth == self.depth:
                return (self.evaluationFunction(gameState), None)

            maxEvaluation = -(float("inf"))
            maxAction = None
            for action in pacmanAct:
                tmpEvaluation, tmpAction = minValue(gameState.generateSuccessor(0, action), 1, depth)
                if tmpEvaluation > maxEvaluation:
                    maxEvaluation = tmpEvaluation
                    maxAction = action
            return maxEvaluation, maxAction

        ##Toi thieu hoa gia tri cua ghost
        def minValue(gameState, ghostIndex, depth):
            ghostAction = gameState.getLegalActions(ghostIndex)
            if len(ghostAction) == 0:
                return self.evaluationFunction(gameState), None

            minEvalution = float("inf")
            minAction = None
            for action in ghostAction:
                ###neu la con ma cuoi cung thi goi ham max
                if ghostIndex == gameState.getNumAgents() - 1:
                    tmpEvalution, tmpAction = maxValue(gameState.generateSuccessor(ghostIndex, action), depth + 1)
                ###neu khong thi goi nhung con ma khac
                else:
                    tmpEvalution, tmpAction = minValue(gameState.generateSuccessor(ghostIndex, action), ghostIndex + 1,
                                                       depth)
                if (tmpEvalution < minEvalution):
                    minAction = action
                    minEvalution = tmpEvalution
            return (minEvalution, tmpEvalution)

        maxAction = maxValue(gameState, 0)[1]
        return maxAction


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def maxValue(gameState, depth, a, b):
            pacmanAct = gameState.getLegalActions(0)

            # Neu khong con duong di hoac thang hoac thua hoac dat den do sau can thiet thi return
            if len(pacmanAct) == 0 or gameState.isWin() or gameState.isLose() or depth == self.depth:
                return (self.evaluationFunction(gameState), None)

            maxEvaluation = -(float("inf"))
            maxAction = None
            for action in pacmanAct:
                tmpEvaluation, tmpAction = minValue(gameState.generateSuccessor(0, action), 1, depth, a, b)
                if tmpEvaluation > maxEvaluation:
                    maxEvaluation = tmpEvaluation
                    maxAction = action
                if maxEvaluation > b:
                    return maxEvaluation, maxAction
                a = max(a, maxEvaluation)

            return maxEvaluation, maxAction

        ##Toi thieu hoa gia tri cua ghost
        def minValue(gameState, ghostIndex, depth, a, b):
            ghostAction = gameState.getLegalActions(ghostIndex)
            if len(ghostAction) == 0:
                return self.evaluationFunction(gameState), None

            minEvalution = float("inf")
            minAction = None
            for action in ghostAction:
                # neu la con ma cuoi cung thi goi ham max
                if ghostIndex == gameState.getNumAgents() - 1:
                    tmpEvalution, tmpAction = maxValue(gameState.generateSuccessor(ghostIndex, action), depth + 1, a, b)
                # neu khong thi goi nhung con ma khac
                else:
                    tmpEvalution, tmpAction = minValue(gameState.generateSuccessor(ghostIndex, action), ghostIndex + 1,
                                                       depth, a, b)
                if (tmpEvalution < minEvalution):
                    minAction = action
                    minEvalution = tmpEvalution
                if minEvalution < a:
                    return minEvalution, minAction
                b = min(b, minEvalution)

            return (minEvalution, minAction)

        a = -(float('inf'))
        b = float('inf')
        maxAction = maxValue(gameState, 0, a, b)[1]
        return maxAction
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

        def maxValue(gameState, depth):
            pacmanAct = gameState.getLegalActions(0)

            # Neu khong con duong di hoac thang hoac thua hoac dat den do sau can thiet thi return
            if len(pacmanAct) == 0 or gameState.isWin() or gameState.isLose() or depth == self.depth:
                return (self.evaluationFunction(gameState), None)

            maxEvaluation = -(float("inf"))
            maxAction = None
            for action in pacmanAct:
                tmpEvaluation, tmpAction = notminValue(gameState.generateSuccessor(0, action), 1, depth)
                if tmpEvaluation > maxEvaluation:
                    maxEvaluation = tmpEvaluation
                    maxAction = action
            return maxEvaluation, maxAction

        def notminValue(gameState, ghostIndex, depth):
            ghostAction = gameState.getLegalActions(ghostIndex)
            if len(ghostAction) == 0:
                return self.evaluationFunction(gameState), None

            averageScore = 0
            minAction = None
            for action in ghostAction:
                if ghostIndex == gameState.getNumAgents() - 1:
                    tmpEvalution = maxValue(gameState.generateSuccessor(ghostIndex, action), depth + 1)
                else:
                    tmpEvalution = notminValue(gameState.generateSuccessor(ghostIndex, action), ghostIndex + 1, depth)
                tmpEvalution = tmpEvalution[0]
                score = tmpEvalution / len(ghostAction)
                averageScore += score
            return (averageScore, minAction)

        maxAction = maxValue(gameState, 0)[1]
        return maxAction

        util.raiseNotDefined()

        util.raiseNotDefined()


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # pacmanPosition = currentGameState.getPacmanPosition()
    # def scoreGhosts():
    score = currentGameState.getScore()
    foods = currentGameState.getFood().asList()
    ghosts = currentGameState.getGhostStates()
    pacmanPosition = currentGameState.getPacmanPosition()
    capsules = currentGameState.getCapsules()

    # dùng các hàm toán học đẻ tính trọng số của các khoảng cách từng tác nhân
    # dùng hàm mũ với khoảng cách giưa pacman và ghost
    for ghost in ghosts:
        distance = manhattanDistance(pacmanPosition, ghost.getPosition())
        if ghost.scaredTimer > 0:
            score += 40.0 / (distance + 1)
        else:
            score -= 2.5 / (distance + 1)

    # dung ham phan so voi khoang cach giua pacman toi thuc an
    foodDistance = []
    for food in foods:
        foodDistance.append(10.0 / manhattanDistance(pacmanPosition, food))
    if len(foodDistance) > 0:
        score += max(foodDistance)
    # dung ham phan so voi khoang cach giua pacman voi thuoc
    capsuleDistance = []
    for capsule in capsules:
        capsuleDistance.append(40.0 / manhattanDistance(pacmanPosition, capsule))
    if len(capsuleDistance) > 0:
        score += max(capsuleDistance)
    return score


# Abbreviation
better = betterEvaluationFunction
