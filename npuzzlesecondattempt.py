# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 09:38:17 2018

@author: Steve
"""

import collections
from datetime import datetime


class puzzle_node:
    
    def __init__(self, board, parent = None):
            self.board = board
            self.parent = parent
            self.hole = self.board.index(0)
    
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
        
    
    #checks if node is equal to goal node
    def solved(self):
        return self.board == list(range(0,9))
    
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
                if j < self.board[i]:
                    bigN += 1
        return bigN % 2 == 0

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
    frontier = collections.deque([start_node])
    explored = set([])
    tries = 0
    while frontier and tries < 5001:
        tries += 1
        current_node = frontier.popleft()
        explored.add(current_node)
        for f in current_node.get_moves():
            new_node = puzzle_node(f(current_node), current_node)
            if new_node.solved():
                print(get_solution(new_node))
                raise ValueError("Solution found.")
            if new_node not in frontier and new_node not in explored:
                frontier.append(new_node)
    raise ValueError("Tries exceeded.")
    
    
    

testnode = puzzle_node([1,2,3,4,0,5,6,7,8])
teststart = puzzle_node([0,1,2,3,4,5,6,7,8])
testnode4 = puzzle_node([0,2,1,5,4,7,6,3,8])
solve_puzzle(testnode)