#!/usr/bin/env python

""" DT179G - LAB ASSIGNMENT 1
The code assignment consists of two parts, and you need to implement a solution for each one based
on the pseudo code presented!
"""

# -----------------------------------------------------------------
# *** ASSIGNMENT 1, PART 1 ***
# -----------------------------------------------------------------
A, B, C = -5, '8', 7.6  # DO NOT MODIFY CONSTANT VALUES
TOTAL = int()           # DO NOT MODIFY DATA TYPE

''' PSEUDO CODE
SUM given values of A, B and C as integers, CASTING where necessary.
STORE result in variable 'TOTAL'.

Expected output:
    -5 + 8 + 7.6 = 10
'''

TOTAL = A + int(B) + int(C)

print("{} + {} + {} = {}".format(A, B, C, TOTAL))  # DO NOT MODIFY

# -----------------------------------------------------------------
# *** ASSIGNMENT 1, PART 2 ***
# -----------------------------------------------------------------
TEXT = "I wrote my very first program at age 10!"   # DO NOT MODIFY CONSTANT VALUES
OUTPUT = str()                                      # DO NOT MODIFY DATA TYPE

''' PSEUDO CODE
DETERMINE whether 'TEXT' contains the value of 'TOTAL' as substring.
IF True STORE "true that" in variable 'OUTPUT' ELSE STORE "nope".

Expected output:
    Value of 'TOTAL' exists in string: true that
'''

if str(TOTAL) in TEXT:
    OUTPUT = "true that"
else:
    OUTPUT = "nope"


print("Value of 'TOTAL' exists in string: {}".format(OUTPUT))  # DO NOT MODIFY
