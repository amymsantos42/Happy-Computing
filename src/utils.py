
import math
import random

def my_normal(mu, sigma):
    u1 = random.random()
    u2 = random.random()
    z = math.sqrt(-2. * math.log(u1)) * math.cos(2. * math.pi * u2)
    return z * math.sqrt(sigma) + mu

def my_exponential(x):
    r = random.random()
    s = (-1 / x) * (math.log( r , math.e ) )
    return s

def my_poisson(x):
    ans = 0
    rand = random.random()

    while(rand > math.e ** -x):
        next_rand = random.random()
        rand *= next_rand
        ans += 1
    return ans
