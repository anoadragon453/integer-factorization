#!/usr/bin/env python3

import math
import numpy
import sys
import os

# Make sure the user provided a number to factor
if len(sys.argv) is not 2:
    print('Please input a single number to factor')
    sys.exit(1)

# Save number
number = sys.argv[1]

# Store first 1000 primes
with open('1000_primes.txt') as primes:
    factorbase = [int(line.rstrip('\n')) for line in primes]


