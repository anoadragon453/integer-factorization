#!/usr/bin/env python3

import math
import numpy as np
import sys
import os
from itertools import product

PRIME_AMT = 10

# Make sure the user provided a number to factor
#if len(sys.argv) is not 2:
#    print('Please input a single number to factor')
#    sys.exit(1)
#
## Save number
#number = sys.argv[1]

# Store first 1000 primes
# We store as a dictionary to allow for fast lookups. Key: prime, value: index
with open('1000_primes.txt') as primes:
    factorbase = {int(line.rstrip('\n')):index for (index, line) in enumerate(primes)}
factorbase = {2:0, 3:1, 5:2, 7:3, 11:4, 13:5, 17:6, 19:7, 23:8, 29:9}
factorbaseL = list(factorbase)
factorbaseL.sort()

number = 16637
def calcR(k, j):
    r = int((k*number)**0.5) + j
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
        
def create_matrix():
    m = np.zeros([PRIME_AMT + 2, PRIME_AMT], dtype=int)
    r_count = 0
    m_rows = set()

    # Calculate r value and whether r^2 is smooth
    for k in range(1, PRIME_AMT**2):
        for j in range(1, k + 1):
            r = calcR(k, j)
            factors = isSmooth(r)
            
            # If we got back the factors, then r^2 is B-smooth
            if factors != []:
                if tuple(factors) not in m_rows: # Check if row is already in matrix
                    for f in factors: # Change matrix row column to 1 if factor is present
                        m[r_count][factorbase[f]] = 1
                    r_count += 1
                    m_rows.add(tuple(factors))
            else:
                # This r^2 value is not B-smooth
                continue
            # Stop when we've populated all rows
            if r_count >= PRIME_AMT + 2:
                break
        if r_count >= PRIME_AMT + 2:
            break

    return m

np.linalg.tensorsolve(create_matrix(),0)


