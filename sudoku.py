from math import sqrt
from copy import deepcopy

class SudokuTable:
    def __init__(self, table):
        self.table = table.copy()
        self.table_len = int(sqrt(len(table)))
        initial_domain = list(range(1, self.table_len + 1))
        self.domain = {}
        for i in range(0, self.table_len):
            for j in range(0, self.table_len):
                if not self.table[i * self.table_len + j]:
                    self.domain[(i, j)] = list(filter(lambda x: x not in self.get_constrains(i, j), initial_domain))

        self.count_empty_variables = table.count(0)

    def __str__(self):
        s = ''
        for i in range(0, self.table_len):
            s=s+str(self.table[i*self.table_len:(i+1)*self.table_len])+'\n'
        return s

    def get_constrains(self, i, j):
        constrains = self.table[i * self.table_len:(i + 1) * self.table_len]

        for a in range(0, self.table_len):
            constrains.append(self.table[a * self.table_len + j])

        a = int(sqrt(self.table_len))
        x = int(i / a)
        y = int(j / a)
        for i in range(x * a, (x + 1) * a):
            for j in range(y * a, (y + 1) * a):
                constrains.append(self.table[i * self.table_len + j])

        constrains = list(set(constrains))
        constrains.remove(0)
        return constrains

    def set_domain_values(self):
        initial_domain = list(range(1, self.table_len + 1))
        self.domain = {}
        for i in range(0, self.table_len):
            for j in range(0, self.table_len):
                if not self.table[i * self.table_len + j]:  # is empty
                    self.domain[(i, j)] = list(filter(lambda x: x not in self.get_constrains(i, j), initial_domain))

    def update_domain(self,i,j,value):
        domain=deepcopy(self.domain)
        for x in range(0,self.table_len):
            if x!=j and domain.get((i,x)) and (value in domain.get((i,x))):
                domain[(i,x)].remove(value)
            if x!=i and domain.get((x,j)) and (value in domain.get((x,j))):
                domain[(x,j)].remove(value)

        a = int(sqrt(self.table_len))
        x = int(i / a)
        y = int(j / a)
        for m in range(x * a, (x + 1) * a):
            for n in range(y * a, (y + 1) * a):
                if (m != i or n!=j) and domain.get((m,n)) and (value in domain.get((m,n))):
                    domain[(m,n)].remove(value)
        return domain

    def set_variable(self, i, j, value):
        self.table[i * self.table_len + j] = value

    def remove_variable(self, i, j):
        self.table[i * self.table_len + j] = 0

    def is_consistent(self,i,j,value):
        constrains=self.get_constrains(i,j)
        if value not in constrains:
            return True
        return False

    def minimum_remaining_value(self):
        min_length = self.table_len
        for i in range(0, self.table_len):
            for j in range(0, self.table_len):
                if self.table[i * self.table_len + j] == 0:
                    if len(self.domain[(i, j)]) < min_length:
                        min_length = len(self.domain[(i, j)])
                        pos = [(i, j)]
                    elif len(self.domain[(i, j)]) == min_length:
                        pos.append((i, j))
        return pos


    def get_unassigned_neighbors(sudoku, i, j):
        neighbors = set()
        size = sudoku.table_len
        row = sudoku.table[size * i: size * (i + 1)]
        neighbors |= set((i, c) for c in range(size) if row[c] == 0 and c != j)
        
        col = [sudoku.table[size * r + j] for r in range(size)]
        neighbors |= set((r, j) for r in range(size) if col[r] == 0 and r != i)
        
        subgrid_size = int(size ** 0.5)
        subgrid_row, subgrid_col = i // subgrid_size, j // subgrid_size
        for r in range(subgrid_row * subgrid_size, (subgrid_row + 1) * subgrid_size):
            for c in range(subgrid_col * subgrid_size, (subgrid_col + 1) * subgrid_size):
                if sudoku.table[size * r + c] == 0 and (r != i or c != j):
                    neighbors.add((r, c))
        
        return neighbors
