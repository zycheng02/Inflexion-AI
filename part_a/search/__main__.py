# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion

from sys import stdin
from .program import search
from .program import move
from .program import update
from .program import Direction
from .program import spread
from .program import check_fin
from .utils import render_board

# WARNING: Do *not* modify any of the code in this file, and submit it as is!
#          You should be modifying the search function in program.py instead.
#
# The code here is used by the autograder to feed your solution input and parse
# the resulting action sequence. Failed test cases due to modification of this 
# file will not receive any marks.
#
# Notice that output is printed to stdout, and all actions are prepended with
# the word "SPREAD". This is to enable the autograder to distinguish between
# the final action sequence and any other output that may be printed to stdout.
# Regardless, you must not print anything to stdout in your *final* submission.

def parse_input(input: str) -> dict[tuple, tuple]:
    """
    Parse input CSV into a dictionary of board cell states.
    """
    return {
        (int(r), int(q)): (p.strip(), int(k))
        for r, q, p, k in [
            line.split(',') for line in input.splitlines() 
            if len(line.strip()) > 0
        ]
    }

def print_sequence(sequence: list[tuple]):
    """
    Print the given action sequence. All actions are prepended with the 
    word "SPREAD", and each action is printed on a new line.
    """
    for r, q, dr, dq in sequence:
        print(f"SPREAD {r} {q} {dr} {dq}")

def main():
    """
    Main entry point for program.
    """
    input = parse_input(stdin.read())
    sequence: list[tuple] = search(input)
    print_sequence(sequence)
    # test move and update:
    # update(input, (5, 6), Direction.UP)
    # update(input, (6, 5), Direction.UP_RIGHT)
    # update(input, (0, 5), Direction.UP)
    # print(render_board(input, ansi=False))
    # print(check_fin(input))

    # test spread:
    # spread(input, (1,3), Direction.DOWN_RIGHT)
    # print(render_board(input, ansi=False))
    # print(check_fin(input))
    # print(check_fin(input, "r"))
    # print(check_fin(input, "b"))

if __name__ == "__main__":
    main()
