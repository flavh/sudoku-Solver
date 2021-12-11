from pycryptosat import Solver
from math import sqrt
import os
solver = Solver()
clear_terminal=lambda: os.system("clear")

def linearize(i, j, k):
    return i*100 + j*10 + k


def delinearize(n):
    i = n//100
    n %= 100
    j = n//10
    n %= 10
    return i, j, n


def atLeastOneInt(solver, max):
    for i in range(1, max):
        for j in range(1, max):
            clause = []
            for n in range(1, max):
                clause.append(linearize(i, j, n))
            solver.add_clause(clause)


def maxOneInt(solver, max):
    for i in range(1, max):
        for j in range(1, max):
            for k in range(1, max):
                for kp in range(k+1, max):
                    solver.add_clause(
                        [-linearize(i, j, k), -linearize(i, j, kp)])


def atLeastOneIntColumn(solver, max):
    for j in range(1, max):
        for k in range(1, max):
            clause = []
            for i in range(1, max):
                clause.append(linearize(i, j, k))
            solver.add_clause(clause)


def atLeastOneIntRow(solver, max):
    for i in range(1, max):
        for k in range(1, max):
            clause = []
            for j in range(1, max):
                clause.append(linearize(i, j, k))
            solver.add_clause(clause)


def atLeastOneIntBlock(solver, max):
    square = int(sqrt(max))
    maxLine = square+1
    maxColumn = square+1
    minLine = 1
    minColumn = 1
    while(maxLine <= max and maxColumn <= max):
        for k in range(1, max):
            clause = []
            for i in range(minLine, maxLine):
                for j in range(minColumn, maxColumn):
                    clause.append(linearize(i, j, k))
            solver.add_clause(clause)
        maxLine += square
        maxColumn += square
        minLine += square
        minColumn += square


max = 10
atLeastOneInt(solver, max)
maxOneInt(solver, max)
atLeastOneIntColumn(solver, max)
atLeastOneIntRow(solver, max)
atLeastOneIntBlock(solver, max)


def entry(solver,max):
    line=1
    column=0
    for i in range(1,(max-1)*(max-1)+1):
        column+=1
        if column==max:
            column=1
            line+=1
        print("Line : ",line," , Column : ",column,". Enter the value : ",end='')
        value=input()
        if(value==""):
            continue
        value=int(value)

        if value>=1 and value < max:
            solver.add_clause([linearize(line,column,value)])
        elif value==42:
            print("Complete automatically.")
            return

entry(solver,max)
success,list_of_variables=solver.solve()
clear_terminal()
if success :
    for i in range(len(list_of_variables)):
        if list_of_variables[i]:
            var=delinearize(i)
            print(var[2],"  ",end='')
            if var[1]==9:
                print()
            else:
                if var[1]%3==0:
                    print("\t", end='')
            if var[0]%3==0 and var[1]==9:
                print()
else:
    print("No solutions.")