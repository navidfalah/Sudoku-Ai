from csp import backtrack
from time import time
from table import table

t=time()
backtrack(table, 1, 0)
t1=time()-t
print(t1)
t=time()
backtrack(table, 2, 1)
t1=time()-t
print(t1)
