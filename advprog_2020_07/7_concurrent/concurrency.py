# concurrency.py
#
# Die Threads! Die Threads!
#
# In this exercise, we consider the problem of implementing concurrency
# from scratch.  This is the same fundamental problem solved by various
# sorts of "async" libraries.
#
# To start, consider the following two functions:

import time

def countdown(n):
    while n > 0:
        print('T-minus', n)
        time.sleep(1)
        n -= 1

def countup(stop):
    x = 0
    while x < stop:
        print('Up we go', x)
        time.sleep(3)
        x += 1

# Normally, functions executed sequentially.  For example, observe
# the output of the following code.

countdown(15)
countup(5)

# -----------------------------------------------------------------------------
# Exercise 1 - Concurrency
#
# Figure out a way for both of the above functions to execute
# concurrently, producing interleaved output like this:
#
#    T-minus 15      (1 sec delay)
#    Up we go 0      (3 sec delay)
#    T-minus 14      (1 sec delay)
#    Up we go 1      (3 sec delay)
#    T-minus 13
#    Up we go 2
#    T-minus 12
#    Up we go 3
#    T-minus 11
#    Up we go 4
#    T-minus 10
#    T-minus 9
#    T-minus 8
#    ...
#    T-minus 1
#
# THE CATCH: You are not allowed import any outside module to do it.
# Moreover, you're not allowed to use any feature of Python other than
# ordinary function calls.  That means no threading, no subprocesses,
# no async, no generators, or anything else. You need to figure out
# how to get something resembling concurrency to work all on your own
# without the support of any library.
# 
# You ARE allowed to change the implementation of the original functions
# and to write any other supporting code you might need to do it--as
# long as that support code only involves normal Python functions.

# -----------------------------------------------------------------------------
# Exercise 2 - Sleeping
#
# In the above code, there were calls to time.sleep().   These are long-running
# calls that block the execution of everything else.  Your task is to reimplement
# the functionality of time.sleep() so that multiple functions can be sleeping
# at the same time and run at different rates.  Specifically, you want the
# output to look something like this where the countdown process is producing
# three times as much output, but both functions finish at the same time.
#
# T-minus 15
# Up we go 0
# T-minus 14
# T-minus 13
# T-minus 12
# Up we go 1
# T-minus 11
# T-minus 10
# T-minus 9
# Up we go 2
# T-minus 8
# T-minus 7
# T-minus 6
# Up we go 3
# T-minus 5
# T-minus 4
# T-minus 3
# Up we go 4
# T-minus 2
# T-minus 1


# -----------------------------------------------------------------------------
# Exercise 3 - Coordination 
#
# With concurrency, you often have tasks that need to coordinate with each
# other in some way.  A common technique for doing that is to use a 
# Queue.  A Queue has methods .put() and .get() that add and remove items
# from the queue respectively.  The .get() method is special in that it
# waits (blocks) until data becomes available if the queue is empty.
#
# Your task: implement a Queue class that works with the concurrency
# code you wrote above.  Then, use it to implement a classic
# producer/consumer problem as illustrated in the following functions
# (pseudocode).
#
# You are not allowed to use any existing Python libraries.  And certainly
# not the built-in threading or queue modules.

def producer(q):
    for i in range(5):
        print('Producing', i)
        q.put(i)
        time.sleep(1)            
    q.put(None)
    print('Producer done')

def consumer(q):
    while True:
        item = q.get()
        if item is None:
            break
        print('Consuming', item)
    print('Consumer done')

def test_prod_cons():
    q = Queue()       # You must define
    run(producer(q))  # Pseudocode
    run(consumer(q))  # Pseudocode

# The expected output of the program is as follows:
#
#     Producing 0
#     Consuming 0
#     Producing 1
#     Consuming 1
#     Producing 2
#     Consuming 2
#     Producing 3
#     Consuming 3
#     Producing 4
#     Consuming 4
#     Producer done
#     Consumer done

