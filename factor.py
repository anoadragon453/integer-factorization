#!/usr/bin/env python3

import math
import numpy

with open('1000_primes.txt') as primes:
    lines = [int(line.rstrip('\n')) for line in primes]
    print (lines)
