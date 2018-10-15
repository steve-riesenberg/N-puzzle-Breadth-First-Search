"""
Created on Wed Oct 10 17:11:56 2018
@author: Steve
"""

import line_profiler

import collections
from datetime import datetime


class puzzle_node:
    
    def __init__(self, board, parent = None):
            self.board = board
            self.parent = parent
            self.hole = self.board.index(0)
            self.man_dist = self.manhattan_distance()
    
    #two nodes are equal if their list representations are equal
    def __eq__(self, other):
        return self.board == other.board
    
    #defining str so we can print nodes
    def __str__(self):
        return str(self.board)
    
    def __hash__(self):
        h = 0
        for value, i in enumerate(self.board):
            h ^= value << i
        return h
    
    def __lt__(self, other):
        return self.man_dist < other.man_dist
    
    #checks if node is equal to goal node
    def solved(self):
        return self.board == list(range(9))
    
    #returns a list of function names of possible moves
    def get_moves(self):
        possible_moves = []
        if self.hole % 3 != 0:
            possible_moves.append(move_left)
        if self.hole % 3 != 2:
            possible_moves.append(move_right)
        if self.hole > 2:
            possible_moves.append(move_up)
        if self.hole < 6:
            possible_moves.append(move_down)
        return possible_moves
     
    #checks to see if the puzzle can be solved by calculating the N value
    #and checking that it is 0 mod 2.
    def solvable(self):
        bigN = 0
        for i in range(9):
            for j in self.board[i+1:]:
                if j < self.board[i] and j != 0:
                    bigN += 1
        return bigN % 2 == 0
    
    def manhattan_distance(self):
        man_dist = 0
        for i in range(1, 9):
            #up down steps calculated by doing integer division with 3
            man_dist += abs((self.board.index(i)//3 - i//3))
            #left right steps calculated by taking mod 3 first then difference
            man_dist += abs((self.board.index(i)%3 - i%3))
        return man_dist
        

def move_up(self):
    copyboard = self.board[:]
    copyboard[self.hole], copyboard[self.hole - 3] = copyboard[self.hole - 3], 0
    return(copyboard)

def move_down(self):
    copyboard = self.board[:]
    copyboard[self.hole], copyboard[self.hole + 3] = copyboard[self.hole + 3], 0
    return(copyboard)
    
def move_left(self):
    copyboard = self.board[:]
    copyboard[self.hole], copyboard[self.hole - 1] = copyboard[self.hole - 1], 0
    return(copyboard)
    
def move_right(self):
    copyboard = self.board[:]
    copyboard[self.hole], copyboard[self.hole + 1] = copyboard[self.hole + 1], 0
    return(copyboard)

def get_solution(start_node):
    #traces back all the parent connections to return the solution
    solution = [start_node]
    while str(solution[0].parent) != "None":
        solution.insert(0, solution[0].parent)
    for i in range(len(solution)):
        solution[i] = solution[i].board
    return solution


def solve_puzzle(start_node):
    if start_node.solved():
        raise ValueError("Puzzle was already solved.")
    if not start_node.solvable():
        raise ValueError("Puzzle is not in solvable class.")
    frontier = [start_node]
    explored = set([])
    tries = 0
    while frontier and tries < 5001:
        tries += 1
        frontier.sort()
        current_node = frontier.pop(0)
        explored.add(current_node)
        for f in current_node.get_moves():
            new_node = puzzle_node(f(current_node), current_node)
            if new_node.solved():
                print(get_solution(new_node))
                raise ValueError("Solution found.")
            if new_node not in frontier and new_node not in explored:
                frontier.append(new_node)
    raise ValueError("Tries exceeded.")
    print("Tries exceeded.")

