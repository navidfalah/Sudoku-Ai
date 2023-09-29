from sudoku import SudokuTable
from copy import deepcopy
from math import sqrt
from queue import PriorityQueue
from table import table


def backtrack(table,SUV,ODV):
    sudoku=SudokuTable(table)
    result=recursive_backtrack({},sudoku,SUV,ODV)
    print(sudoku)


def recursive_backtrack(assignment, sudoku, SUV, ODV):
    if len(assignment) == sudoku.count_empty_variables:
        return assignment
    i, j = select_unassigned_variable(sudoku, choice=SUV)
    last_domain = deepcopy(sudoku.domain)
    for value in order_domain_values(sudoku, choice=ODV, i=i, j=j):
        if sudoku.is_consistent(i, j, value):
            assignment[(i, j)] = value
            sudoku.set_variable(i, j, value)
            sudoku.domain = deepcopy(last_domain)
            sudoku.domain = sudoku.update_domain(i, j, value)
            result = recursive_backtrack(assignment, sudoku, SUV, ODV)
            if result:
                return result
            assignment.pop((i, j))
            sudoku.domain = deepcopy(last_domain)
            sudoku.remove_variable(i, j)
    return False


def select_unassigned_variable(sudoku, choice):
    if choice == 0:
        pos = sudoku.table.index(0)
        return int(pos / sudoku.table_len), int(pos % sudoku.table_len)

    if choice == 1:
        pos = sudoku.minimum_remaining_value()
        return pos[0]

    if choice == 2:
        pos = sudoku.minimum_remaining_value()
        return degree_heuristic(sudoku, pos)


def order_domain_values(sudoku, choice, i, j):
    if choice == 0:
        return sorted(sudoku.domain[(i, j)])
    if choice == 1:
        return least_constraint_value(sudoku,i,j)


def least_constraint_value(sudoku, i, j):
    values = PriorityQueue()
    for value in sudoku.domain[(i, j)]:
        new_domain = sudoku.update_domain(i, j, value)
        constraint = sum(len(new_domain[key]) for key in new_domain.keys())
        values.put((constraint, value))
    ordered_domain = [values.get()[1] for _ in range(values.qsize())]
    ordered_domain.reverse()
    return ordered_domain


def degree_heuristic(sudoku, empty_positions):
    max_degree_pos = None
    max_degree = -1
    
    for i, j in empty_positions:
        neighbors = sudoku.get_unassigned_neighbors(i, j)
        degree = len(neighbors)
        
        if degree > max_degree:
            max_degree = degree
            max_degree_pos = (i, j)
            
    return max_degree_pos
