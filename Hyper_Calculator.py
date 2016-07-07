import math
from fractions import *

def smallernum(a,b):
    '''Return the smaller of two values'''
    if a < b: return a
    else: return b

def Odds(a,b,d):
    '''Returns probability

    Parent: HGC()
    Called when: sample size is 1
    Why: Prevents factorials from being made, as it is unnecessary. Of course,
    computers are so fast this method probably isn't necessary anyway.
    '''
    if d == 1: return Fraction(b,a)
    else: return Fraction(a-b,a)

def P(n, r):
    '''Returns nPr as a fraction'''
    if (r>n): return 0
    else: return Fraction(math.factorial(n),math.factorial(n - r))

def C(n, r):
    '''Returns nCr as a fraction'''
    if (r>n): return 0
    else: return Fraction(P(n,r),math.factorial(r))
    # return math.factorial(n) / (math.factorial(r) * math.factorial(n - r)

def HGC(a,b,c,d):
    '''Hyper Geometric Calculator

    Variables
    a: Population size
    b: Possible sucesses
    c: Sample size
    d: # of successes
    '''
    if (b>a) | (c>a) | (d>a) | (d>c): return 0
    elif c == 1: return Odds(a,b,d)
    else: return Fraction(C(b,d)*C(a-b,c-d),C(a,c))

def HGCC(a,b,c,d,find="="):
    '''Hyper Geometric Cumulative Calculator

    Calls HGC() multiple times, based on the "find" modifier
    Variables

    a: Population size
    b: Possible successes
    c: Sample size
    d: # of successes
    find: modifies variable d. Available inputs; < ,<= ,> , >=, =
    '''
    if find == "<":
        x = 0
        for i in range(d): x += HGC(a,b,c,i)
        return x
    elif find == "<=":
        x = 0
        for i in range(d+1): x += HGC(a,b,c,i)
        return x
    elif find == ">":
        x = 0
        f = smallernum(c,b)
        for i in range(d+1,f+1): x += HGC(a,b,c,i)
        return x
    elif find == ">=":
        x = 0
        f = smallernum(c,b)
        for i in range(d,f+1): x += HGC(a,b,c,i)
        return x
    else: return HGC(a,b,c,d)

def quickodds(a,b,c,d):
    '''Displays all probabilities of a given value

    Calls all modifiers of HGCC()

    Variables
    a: Population size
    b: Possible successes
    c: Sample size
    d: # of successes
    '''
    print("              Chance to get exactly {}: {}".format(d,HGCC(a,b,c,d,find="=")))
    print("                Chance to less than {}: {}".format(d,HGCC(a,b,c,d,find="<")))
    print("Chance to get less than or equal to {}: {}".format(d,HGCC(a,b,c,d,find="<=")))
    print("                Chance to more than {}: {}".format(d,HGCC(a,b,c,d,find=">")))
    print("Chance to get more than or equal to {}: {}".format(d,HGCC(a,b,c,d,find=">=")))

def cascadeodds(a,b,c):
    '''Print exact odds for each # of successes'''
    for i in range(0,c+1): print("Chance to get exactly {}: {}".format(i,HGC(a,b,c,i)))
