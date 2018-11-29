import numpy as np
import sys
import os
import subprocess
import math
from decimal import Decimal

def log(*args):
    if debug:
        print(*args)

# createFactorbase returns a dict of prime numbers with a
# given length L
# We store our factorbase as a dictionary as we need to find
# out the index of a factor later with only the factor itself
# Storing as a list, we'd need to iterate over the list many
# times to find that factors index, but with a dict this can
# be a constant time lookup
def createFactorbase(L):
    factorbase = {}
    count = 0

    # Open primes.txt, load in primes line by line
    with open('primes.txt') as primes:
        for prime in primes:
            if count >= L:
                return factorbase

            # Additionally include an incrementing index for
            # later quick reference
            factorbase[int(prime.strip())] = count
            count += 1

# calcR generates an r value according to equation 1,
# given input values j and k
def calcR(j, k):
    r = int((k*number)**0.5) + j
    return r

# generateSmoothFactors creates a dictionary of factors and
# their exponents from a number r. It derives factors
# from a given factorbase, f.
# If the number is not B-Smooth, it returns None
def generateSmoothFactors(r, f, N):
    # Calculate r^2 within our modulo
    r2 = (r*r) % N

    # Dictionary of factors we will return
    factors = {}

    # Iterate over our factorbase and create a list of
    # factors.
    for prime in f.keys():
        # Check if this prime factors into r^2
        # Keep doing so and reducing r^2 by that factor until
        # We can no longer do so with this prime
        while r2 > 1 and r2 % prime is 0:
            # Add prime to the dict of factors, or increment
            # its exponent if it's already present
            if prime in factors:
                factors[prime] += 1
            else:
                factors[prime] = 1

            # Reduce r2 by this prime
            r2 = r2 // prime
            log("Reduced r2 to:", r2)

    log("Retrieved factors for %d:" % ((r*r) % N))
    log(factors)
           
    # If r2 is 1, then r is B-smooth
    if r2 is 1:
        factors_list = []

        # Return only the factors with odd exponents
        for factor, exponent in factors.items():
            # Check and add only if exponent is odd
            if exponent % 2 is 1:
                factors_list.append(factor)

        return factors
    else:
        # Return None if not B-smooth.
        # We will be discarding this prime
        return None

#####################################
##          Program Start          ##
#####################################

# Whether to enable or disable debug printing
# No printing means a faster runtime
debug = False

# The amount of primes in our factorbase
prime_amount = 1000

# The amount of r values, directly proportionate to our
# factorbase length
r_amount = prime_amount + 10

# The number to factor
number = 3205837387

# Our factorbase, which holds the first prime_amount primes
log('Creating factorbase...')
factorbase = createFactorbase(prime_amount)
log("Factorbase:", factorbase)

# Create rows to fill our binary matrix with.
# Once the list is filled, insert those rows which are unique
# into our binary matrix
rows = []

# We also create a list to store the corresponding factors
# so that we can later multiply these factors together
factors_record = []

# And finally, we keep a record of all of our chosen r values.
# We'll also need to multiply these together towards the end
r_values = []

# Iterate over values generated by calcR, checking whether
# each one is B-smooth according to our factorbase.
# If so, add its factors as a row to rows, and thus our
# binary matrix
(j, k) = (2, 3)
log("Generating rows...")
while len(rows) < r_amount:
    r = calcR(j, k)
    log("Got r value:", r)
    log("Generating factors...")

    # Check if this number is B-smooth
    factors = generateSmoothFactors(r, factorbase, number)
    if factors:
        # The number is smooth, include the factors in our
        # binary matrix

        # Retrieve the indexes of these factors in our
        # factorbase
        indexes = list(map(lambda factor: factorbase[factor], factors))

        # Create a list of zeros to store binary encoded indexes
        row = [False] * prime_amount

        # Set each value in our row to True (binary 1) that
        # corresponds to an odd factor
        for index in indexes:
            row[index] = True

        # Add the row to our matrix, but only if it is unique
        if row not in rows:
            rows.append(row)
            log('Added row:', row)

            # Also save these factors to a list for later
            factors_record.append(factors)

            # And the r value
            r_values.append(r)

    k += 1
    if k > 30:
        j += 1
        k = 2

# Create a binary matrix of size r_amount x prime_amount
# dtype is boolean to represent a binary value
matrix = np.zeros([r_amount, prime_amount], dtype=bool)

# We will now fill our matrix with our binary rows of factors.
rows = rows
for i in range(r_amount):
    matrix[i] = rows[i]

log('Our binary matrix:')
log(matrix)

# Use an external program to solve the system of equations our
# binary matrix represents for x and y
in_file = 'matrix.txt'
out_file = 'matrix-out.txt'
executable = './GaussBin.exe'

# Export matrix to text file format
with open(in_file, 'w') as f:
    f.write('%d %d' % matrix.shape)
    f.write('\n')
    for row in matrix:
        for item in row:
            f.write('%d ' % int(item))
        f.write('\n')

# Perform Gaussian elimination on matrix
subprocess.run([executable, in_file, out_file])

# Read in modified matrix
lines = [line.rstrip() for line in open(out_file)]

# Get shape of this new matrix
row_count = int(lines[0])
col_count = r_amount

# Reduce lines to just the matrix's contents
lines = lines[1:]

# Feed items into a new numpy matrix
new_matrix = np.zeros([row_count, col_count], dtype=int)
for index, line in enumerate(lines):
    items = line.split(' ')

    # Insert list of items into numpy matrix
    new_matrix[index,] = np.array(items)

# Remove temporary files
os.remove(in_file)
os.remove(out_file)

log("Our new matrix is:")
log(new_matrix)

# Each row of this new matrix is a clue to solving this
# system of equations. In each row, the value of every column
# specifies which of our list of factors in our original
# system of equations we need to multiply together to find
# a factor
for row in new_matrix:
    # This will be our resulting right side of the
    # row multiplication equation.
    # This is created by multiplying all the factors
    # from all the specified rows together
    right_product = 1

    # And this will be our left, made up from all the
    # r values multiplied together
    left_product = 1

    # Go through each value in this row of the matrix
    for index, item in enumerate(row):
        # If the value is 1, that means we will use the
        # list of factors that corresponds to the index
        # of this value in the row
        if item == 1:
            # Get the r value this corresponds to and add it
            # to the left product
            left_product *= r_values[index]**2
            
            # Then get the dict of factors for this r value.
            # This contains the factors and their exponents
            # as keys and values of a dictionary
            factors = factors_record[index]

            # Iterate through the dict, pulling out each
            # number and multiplying them together with the
            # value of the right product
            for factor, exponent in factors.items():
                right_product *= factor**exponent

    # Now we sqrt the products, and keep them in the modulo
    left_product = int(Decimal(left_product).sqrt()) % number
    right_product = int(Decimal(right_product).sqrt()) % number

    log('Left: %d, right: %d' % (left_product, right_product))

    # Now we calculate gcd(right - left, number)
    # If the gcd is 1 or number, then we didn't find a factor.
    # Otherwise, we did, and we're done!
    factor = math.gcd(right_product - left_product, number)
    if factor != 1 and factor != number:
        # We found a factor, yay! Return it and the number
        # divided by the factor to find the other one
        other_factor = number / factor

        # Print out our factors
        print('(%d, %d)' % (factor, other_factor))

        # Exit the program
        sys.exit(0)