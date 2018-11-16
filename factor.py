#!/usr/bin/env python3

import math
import numpy as np
import sys
import os
from itertools import product

PRIME_AMT = 1000

# Make sure the user provided a number to factor
if len(sys.argv) is not 2:
    print('Please input a single number to factor')
    sys.exit(1)

# Save number
number = sys.argv[1]

# Store first 1000 primes
# We store as a dictionary to allow for fast lookups. Key: prime, value: index
with open('1000_primes.txt') as primes:
    factorbase = {int(line.rstrip('\n')):index for (index, line) in enumerate(primes)}

# Calculate a binary matrix with rows being (r?) and columns being indexes in
# our factorbase. Initialize filled with zeros
m = np.zeros([PRIME_AMT + 2, PRIME_AMT])

# Keep track of how many rows we've filled and stop when we've filled them all
r_count = 0

for j, k in product(range(PRIME_AMT), range(PRIME_AMT)):
    # Calculate r value and whether r^2 is smooth
    r = calcR(j, k)
    factors = isSmooth(r)

    # If we got back the factors, then r^2 is B-smooth
    if factors is not None:
        # Change matrix row column to 1 if factor is present
        for f in factors:
            m[r_count, factorbase[f]] = 1
        r_count += 1
    else:
        # This r^2 value is not B-smooth
        continue

    # Stop when we've populated all rows
    if r_count >= m.shape[0]:
        break

