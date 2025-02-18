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
from typing import List
from typing import Optional
from typing import Union
from typing import Callable
from typing import NewType

from game import Directions

Fringe = NewType('Fringe', Union[util.Queue, util.Stack, util.PriorityQueue])

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

class Node(object):
    """This class holds information about a node used in a graph search
    
    Attributes:
        state: A search state.
        parent: The parent Node of this node
        action: The action used to get to the current state from the parent state
    """

    def __init__(self,
                 state: any,
                 parent: Optional['Node'] = None,
                 action: Optional[Directions] = None,
                 costFromParent: Optional[int] = 1) -> None:
        """Inits Node with a state and parent."""
        self.state = state
        self.parent = parent
        self.action = action
        self.costFromParent = costFromParent
    
    @property
    def directions(self) -> List[Directions]:
        """Gets the directions to the state."""
        return self._get_directions()
    
    def _get_directions(self) -> List[Directions]:
        """Indirect accessor to calculate the 'directions' property."""
        if self.parent is None:
            return []
        else:
            return self.parent.directions + [self.action]
    
    @property
    def costFromRoot(self) -> int:
        if self.parent is None:
            return self.costFromParent
        else:
            return self.parent.costFromRoot + self.costFromParent
    
    def __str__(self) -> str:
        return "Node at (%s)" % (", ".join(map(str, self.state)))

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def _graph_search(problem: SearchProblem,
                  fringe: Fringe,
                  strategy: Callable[[Fringe, Node], None]) -> Node:
    """Preforms a graph search on a problem using a given fringe and strategy.

    Args:
        problem: The problem being solved
        fringe: A storage system for nodes to be saved in
        strategy: A function for how to add items to the fringe

    Returns:
        Goal Node found at the end of the search.
    """
    closed = set()
    strategy(fringe, Node(problem.getStartState()))
    
    while(not fringe.isEmpty()):
        node = fringe.pop()
        if problem.isGoalState(node.state): return node
        if node.state not in closed:
            closed.add(node.state)
            for successor in problem.getSuccessors(node.state):
                strategy(fringe, Node(successor[0], node, successor[1], successor[2]))

def depthFirstSearch(problem):
    """Search the deepest nodes in the search tree first."""
    def strategy(fringe: Fringe, node: Node):
        fringe.push(node)

    return _graph_search(problem, util.Stack(), strategy).directions

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    def strategy(fringe: Fringe, node: Node):
        fringe.push(node)

    return _graph_search(problem, util.Queue(), strategy).directions

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    def strategy(fringe: Fringe, node: Node):
        fringe.push(node, node.costFromRoot)

    return _graph_search(problem, util.PriorityQueue(), strategy).directions

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    def strategy(fringe: Fringe, node: Node):
        fringe.push(node, node.costFromRoot + heuristic(node.state, problem))

    return _graph_search(problem, util.PriorityQueue(), strategy).directions


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
