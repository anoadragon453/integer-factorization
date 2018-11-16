#!/usr/bin/env python3

import math
import numpy
import sys
import os

# Make sure the user provided a number to factor
##if len(sys.argv) is not 2:
##    print('Please input a single number to factor')
##    sys.exit(1)
##
### Save number
##number = sys.argv[1]

# Store first 1000 primes
with open('1000_primes.txt') as primes:
    factorbase = [int(line.rstrip('\n')) for line in primes]
    
def calcR(j, k, number):
    r = int((k*number)^0.5) + j
    return r

number = 16637
def isSmooth(r):
    r2 = r*r % number
    factors = []
    index = len(factorbase) - 1
    for prime in list(factorbase)[::-1]:
        if r2 % prime == 0:
            if (not(factors == [])) and prime == factors[0]:
                factors.remove(prime)
            else:
                factors.insert(0, prime)
            r2 = r2 / prime
        else:
            index -= 1
    if r2 in factorbase:
        factors.insert(0, int(r2))
        return (True, factors)
    else:
        return None
    
