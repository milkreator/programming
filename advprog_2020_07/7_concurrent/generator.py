# generator.py
#
# An alternative approach to the concurrency approach is to use a 
# clever hack involving generator functions.  Normally, generator
# functions are used for custom iteration patterns.  For example:
#
#     def countdown(n):
#         while n > 0:
#             yield n
#             n -= 1
# 
#     for x in countdown(5):
#         print('T-minus', x)
#
#
# However, they can also be used to implement concurrency. 
# Consider the following two generators:

import time

def countdown(n):
    while n > 0:
        print('T-minus', n)
        time.sleep(1)
        n -= 1
        yield

def countup(stop):
    x = 0
    while x < stop:
        print('Up we go', x)
        time.sleep(3)
        x += 1
        yield

# These are the same two functions that you had in the last part.
# Just one extra "yield" statement has been added.   Here's an
# example of running the two functions concurrently.

def run_generators():
    generators = [ countdown(15), countup(5) ]
    while generators:
        gen = generators.pop(0)
        try:
            next(gen)
            generators.append(gen)
        except StopIteration:
            pass

run_generators()         # Comment out later

# -----------------------------------------------------------------------------
# Exercise 4
#
# Now, you might be thinking... maybe we could reinvent our whole
# approach to concurrency to use generator functions instead of all of
# that mess with callbacks.  You would be wrong.  Your challenge is to
# define a single class "Task" that wraps a generator and makes it run
# IN THE CONCURRENCY CODE YOU ALREADY WROTE (concurrency.py).  You are
# not allowed to change that code in any way.  You can only import it
# here.  Moreover, you're not allowed to change any of the above
# generator functions either.

class Task:
    ...   # You implement.  This class is the only code you can define.


def run_tasks():
    import concurrency
    t1 = Task(countdown(15))
    t2 = Task(countup(5))
    # Make t1 and t2 run concurrently using earlier code. No modifications.
    # concurrency.???               
    # concurrency.???
    # concurrency.run(???)

# run_tasks()          # Uncomment

# -----------------------------------------------------------------------------
# Exercise 5
#
# What about the time.sleep() calls in the above code.   Is there some way
# to implement that functionality in some way that actually works?  (Meaning
# that the countdown generator produces output 3 times faster than the 
# countup generator).  
#
# Your task is to implement a generator based sleep() function below.
# This function can only use a single "yield" statement with no
# arguments.  It can only use functionality that you already wrote and
# possibly the Task class above.

def sleep(seconds):
    ...    # You implement
    yield

# The countdown() and countup() functions will be modified to use "yield from"
# as follows.  Note: "yield from" is a way to make one generator call
# another one as a kind of subroutine.

def countdown(n):
    while n > 0:
        print('T-minus', n)
        yield from sleep(1)
        n -= 1

def countup(stop):
    x = 0
    while x < stop:
        print('Up we go', x)
        yield from sleep(3)
        x += 1

# Try running these tasks using the run_tasks() above. See if you get
# the right behavior.

# run_tasks()       # Uncomment

