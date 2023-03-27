# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion

from .utils import render_board
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
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0
    def __eq__(self, other):
        return self.position == other.position


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
    Update the game board after token movement.
    """
    new_board = board.copy()
    token = new_board[pos]
    colour, power = token
    if spread:
        power = 1
    d_pos = move(new_board, pos, move_direction)
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
    for i in range(power):
        new_pos = move(new_board, curr_pos, move_direction)
        new_board = update(new_board, curr_pos, move_direction, True)
        curr_pos = new_pos
    new_board.pop(pos)
    return new_board

def check_fin(board: dict[tuple, tuple]):
    if board != None:
        tokens = list(board.values())
        win_colour = tokens[0][0]
        for i in tokens:
            if i[0] != win_colour:
                return False
    return win_colour

def search(input: dict[tuple, tuple]) -> list[tuple]:
    """
    This is the entry point for your submission. The input is a dictionary
    of board cell states, where the keys are tuples of (r, q) coordinates, and
    the values are tuples of (p, k) cell states. The output should be a list of 
    actions, where each action is a tuple of (r, q, dr, dq) coordinates.

    See the specification document for more details.
    """
    # Create start node list
    start_node_list=
    # Initialize both open and closed list

    # Add the start node

    # Loop until you find the end

        # get the current node


    # The render_board function is useful for debugging -- it will print out a 
    # board state in a human-readable format. Try changing the ansi argument 
    # to True to see a colour-coded version (if your terminal supports it).
    print(render_board(input, ansi=False))

    # Here we're returning "hardcoded" actions for the given test.csv file.
    # Of course, you'll need to replace this with an actual solution...
    return [
        (5, 6, -1, 1),
        (3, 1, 0, 1),
        (3, 2, -1, 1),
        (1, 4, 0, -1),
        (1, 3, 0, -1)
    ]
