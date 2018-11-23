#!/usr/bin/env python3

import math
import numpy as np
import sys
import os
import subprocess
from itertools import product

PRIME_AMT = 1024

# Make sure the user provided a number to factor
#if len(sys.argv) is not 2:
#    print('Please input a single number to factor')
#    sys.exit(1)
#
## Save number
#number = sys.argv[1]

# Store first 1000 primes
# We store as a dictionary to allow for fast lookups. Key: prime, value: index
with open('primes1024.txt') as primes:
    factorbase = {int(line.rstrip('\n')):index for (index, line) in enumerate(primes)}
#factorbase = {2:0, 3:1, 5:2, 7:3, 11:4, 13:5, 17:6, 19:7, 23:8, 29:9}
#factorbase.pop(7907)
factorbaseL = list(factorbase)


factorbaseL.sort()
#print (factorbaseL)
print (len(factorbaseL))
number = 3205837387
def calcR(k, j):
    r = int(round((k*number)**0.5)) + j
    return r


def isSmooth(r):
    #initialize values
    r2 = (r*r) % number
    factors = []
    index = len(factorbaseL) - 1

    #iterate over factor base and create list of factors
    while index != -1:
        prime = factorbaseL[index]
        if r2 % prime == 0:
            if (not(factors == [])) and prime == factors[0]:
                factors.remove(prime) #remove x^2 elements
            else:
                factors.insert(0, prime)
            r2 = r2 // prime
        else:
            index -= 1
            #print (index)
           

    #r2 will be one if r is B-smooth
    if r2 == 1:
        return factors
    else:
        return []
    
# Calculate a binary matrix with rows being (r?) and columns being indexes in
# our factorbase. Initialize filled with zeros
#m = np.zeros([PRIME_AMT + 2, PRIME_AMT], dtype=int)

# Keep track of how many rows we've filled and stop when we've filled them all
#r_count = 0

rowIndex_to_rValue = dict()

def create_matrix():
    m = np.zeros([PRIME_AMT + 10, PRIME_AMT], dtype=int)
    r_count = 0
    m_rows = set()

    # Calculate r value and whether r^2 is smooth
    for k in range(1, PRIME_AMT**2):
        for j in range(1, k + 1):
            #if k > 124:
              #  print(k)
            r = calcR(k, j)
            factors = isSmooth(r)
            
            # If we got back the factors, then r^2 is B-smooth
            if factors != []:
                if tuple(factors) not in m_rows: # Check if row is already in matrix
                    for f in factors: # Change matrix row column to 1 if factor is present
                        m[r_count][factorbase[f]] = 1
                    r_count += 1
                    print(r_count)
                    m_rows.add(tuple(factors))
                    rowIndex_to_rValue[r_count - 1] = r
                else:
                    continue
            else:
                # This r^2 value is not B-smooth
                continue
            # Stop when we've populated all rows
            #print(r_count)
            if r_count >= PRIME_AMT + 10:
                break
        if r_count >= PRIME_AMT + 10:
            break

    return m

matrix = create_matrix()

# Export matrix to text file format
with open('matrix.txt', 'w') as f:
    f.write('%d %d' % matrix.shape)
    f.write('\n')
    for row in matrix:
        for item in row:
            f.write('%d ' % int(item))
        f.write('\n')

# Perform Gaussian elimination on matrix
subprocess.run(["./GaussBin.exe", "matrix.txt", "matrix-out.txt"])

# Read in modified matrix
lines = [line.rstrip() for line in open('matrix-out.txt')]

# Get number of rows
row_count = int(lines[0])
col_count = PRIME_AMT + 10

# Skip row count when looping through matrix contents
lines = lines[1:]

# Feed items into numpy matrix
new_matrix = np.zeros([row_count, col_count], dtype=int)
for index, line in enumerate(lines):
    items = line.split(' ')

    # Insert list of items into numpy matrix
    new_matrix[index,] = np.array(items)

#print(new_matrix)


def calcPrimes():
    temp = 1
    for j in range((new_matrix.shape)[0]): # may iterate out of bounds if no value found
        rowL = []
        for i in range(col_count):
            if new_matrix[j][i] == 1:
                rowL.append(i)
        left = 1
        right = 1
        #print(rowL)
        for num in rowL:
            left = left * rowIndex_to_rValue[num]
            right = right * (((rowIndex_to_rValue[num])**2) % number)
        right = math.log(right)
        right = math.sqrt(right)
        right = math.exp(right)
        left = left % number
        right = int(round(right)) % number
        #print(left)
        #print(right)
        factor1 = math.gcd(abs(right - left), number)
        #print(factor1)
        #print (temp)
        temp += 1
        #print(factor1)
        #print(left)
        #print(right)
        #print("\n")
        if factor1 != 1:
            factor2 = number//factor1
            #print (factor1)
            return (factor1, factor2)
