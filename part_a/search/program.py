# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion

import time
from enum import Enum

class Direction(Enum):
    UP = (1, -1)
    UP_RIGHT = (1, 0)
    DOWN_RIGHT = (0, 1)
    DOWN = (-1, 1)
    DOWN_LEFT = (-1, 0)
    UP_LEFT = (0, -1)

class Node():
    """A node class for A* Pathfinding"""
    def __init__(self, parent=None, action=None, board=None, nodeNo=None):
        self.parent = parent
        self.action = action
        self.board = board
        self.nodeNo = nodeNo
        self.g = 0
        self.h = 0
        self.f = 0
    def __eq__(self, other):
        return (self.nodeNo == other.nodeNo)


def move(board: dict[tuple, tuple], pos, direction) -> tuple:
    """
    Compute the end coordinates of the token movement towards given direction.
    """
    r, q = pos
    r_change, q_change = direction.value
    #calculate the new position of the token
    new_r = r + r_change
    new_q = q + q_change

    #check if the new position reaches board boundary
    if new_r > 6:
        new_r = 0
    elif new_r < 0:
        new_r = 6
    if new_q < 0:
        new_q = 6
    elif new_q > 6:
        new_q = 0

    return (new_r, new_q)

def update(board: dict[tuple, tuple], pos, move_direction = None, spread=False) -> dict[tuple, tuple]:
    """
    Update the game board for a single token movement.
    """
    new_board = board.copy()
    token = new_board[pos]
    colour, power = token
    if spread:
        power = 1
    # updated position
    d_pos = move(new_board, pos, move_direction)
    # updated board
    if d_pos in new_board:
        d_token = new_board[d_pos]
        d_power = d_token[1]
        power += d_power

    if not spread:
        new_board.pop(pos)
    new_board[d_pos] = (colour, power)
    return new_board

def spread(board: dict[tuple, tuple], pos, move_direction):
    new_board = board.copy()
    token = new_board[pos]
    power = token[1]
    curr_pos = pos
    powerOverflow=[]
    # iterate movement for all positions, creating n tokens for power level n of token being spread in given direction
    for i in range(power):
        if curr_pos in new_board:
            new_pos = move(new_board, curr_pos, move_direction)
            new_board = update(new_board, curr_pos, move_direction, True)

            # power bigger than 6, add token to removal list to be removed after spread completion
            if (new_board[new_pos][1] >6):
                powerOverflow.append(new_pos)
            
            curr_pos = new_pos

    for i in powerOverflow: 
        new_board.pop(i)

    new_board.pop(pos)
    return new_board

def check_fin(board: dict[tuple, tuple]):
    if board != None:
        tokens = list(board.values())
        win_colour = 'r'
        # if all tokens left on board are same colour - win condition
        for i in tokens:
            if i[0] != win_colour:
                return False

    return win_colour

def possible_actions(board: dict[tuple, tuple], colour):
    list_actions = []
    for token in board:
        curr_colour = board[token][0]
        if curr_colour == colour:
            for direction in Direction:
                # action is (token, direction) tuple
                list_actions.append((token, direction))
    return list_actions

def calc_heuristics(board: dict[tuple, tuple], action):
    pos, direction = action
    new_board = spread(board, pos, direction)
    tokens = [(r, q) for r, q in new_board.keys() if new_board[(r,q)][0] == 'b']
    repeat = []

    if len(tokens) == 1:
        return 1
    
    for blue in tokens:
        for dir in Direction:
            curr_coord = blue
            for i in range(6):
                new_coord = move(new_board, curr_coord, dir)
                if new_coord in tokens:
                    tokens.remove(new_coord)
                curr_coord = new_coord
        
    # end up with token amount = amount of distinct lines
    num_lines = len(tokens)
    return 2*num_lines

"""
The following code was implemented based on the A* pathfinding pseudocode
by Nicholas Swift
https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
"""
def a_star(board: dict[tuple, tuple]):
    start = time.time()
    open_list = []
    
    nodecount = 0
    nodecount+=1
    # create initial node to add to search list
    new_node = Node(None, None, board,nodecount)
    new_node.g = new_node.h = new_node.f = 0
    open_list.append(new_node)
        
    closed_list = []
    # begin search
    while len(open_list) > 0:
        curr_node = open_list[0]
        curr_index = 0

        for i in range(len(open_list)):
            # find next lowest cost (f) move - acts like pq
            if open_list[i].f < curr_node.f:
                curr_node = open_list[i]
                curr_index = i

        # choose node with smallest f value to explore, add to visited list (closed)
        open_list.pop(curr_index)
        closed_list.append(curr_node)

        # check if won state - only red tokens left on board 
        if (check_fin(curr_node.board) == 'r'):
            path = []
            curr = curr_node
            spreadcount = 0
            # back track to get path
            while curr is not None and curr.action is not None:
                spreadcount +=1
                direction_coord = curr.action[1].value
                action_tup = (curr.action[0][0], curr.action[0][1], direction_coord[0], direction_coord[1])
                path.append(action_tup)
                curr = curr.parent
            end = time.time()
            return path[::-1]
        
        # not won - explore 1 layer deeper generating child nodes
        children = []
        list_actions = possible_actions(curr_node.board, 'r')

        # generates 6n child nodes where n is number of red tokens
        for new_action in list_actions:
            nodecount+=1
            new_board = spread(curr_node.board, new_action[0], new_action[1])
            new_child_node = Node(curr_node, new_action, new_board, nodecount)
            new_child_node.h = calc_heuristics(curr_node.board, new_action)
            children.append(new_child_node)
        

        for child in children:
            # if visited, go to next iteration of search loop 
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            child.g = child.parent.g + 1
            child.f = child.g + child.h
            # if any nodes in open list that is one layer above child, go to next iteration of search loop
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            open_list.append(child)


def search(board: dict[tuple, tuple]) -> list[tuple]:
    """
    This is the entry point for your submission. The input is a dictionary
    of board cell states, where the keys are tuples of (r, q) coordinates, and
    the values are tuples of (p, k) cell states. The output should be a list of 
    actions, where each action is a tuple of (r, q, dr, dq) coordinates.

    See the specification document for more details.
    """
    steps = a_star(board)


    # The render_board function is useful for debugging -- it will print out a 
    # board state in a human-readable format. Try changing the ansi argument 
    # to True to see a colour-coded version (if your terminal supports it).
    # print(render_board(board, ansi=False))

    # Here we're returning "hardcoded" actions for the given test.csv file.
    # Of course, you'll need to replace this with an actual solution...
    return steps
