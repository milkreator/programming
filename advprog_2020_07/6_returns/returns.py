# returns.py
#
# Objective: Explore function evaluation, delayed evaluation, error
# handling, composition of operations, and the problem of
# communicating results.  Plus, a tiny bit of concurrency.
# -----------------------------------------------------------------------------
#
# Mary has been pondering the mysteries of the universe, time, and
# function evaluation. In this project, we're going to sneak in and
# join her.  Let's peek inside her mind...
#
# ... ah, we see that Mary is currently pondering the following
# function.  It accepts a time delay and a function callback.  The
# evaluation of the supplied function is delayed and its result
# returned. Very exciting! Maybe it's meant to make a normal function
# mimic the performance of a microservice in the "cloud."

import time

def after(seconds, func):
    time.sleep(seconds)
    return func()

# ------------------------------------------------------------------------------
# Exercise 1
#
# Try calling the above function with a simple "Hello World" example. Make
# sure you understand how it works.
# -----------------------------------------------------------------------------

def greeting():
    print('Hello World')

# How do you use the greeting() function with the after() function above?
# That is, have the after() function call greeting() after 10 seconds.

# -----------------------------------------------------------------------------
# Exercise 2
#
# It seems that the after() function only works if you give it a
# function taking no arguments.  Is there any way to make it work with
# a function that takes any set of arguments?  Can you do this without
# making any code changes?

def add(x, y):
    print(f'Adding {x} + {y} -> {x + y}')
    return x + y

# This doesn't work. Why?  Can you fix it in some way?
# result = after(10, add(2, 3))            # Uncomment


# -----------------------------------------------------------------------------
# Exercise 3
#
# You're the designer of the after() function.  What is your suggested
# "best solution" for making the function easy to use with any
# function that a user might provide?
#
# This is a surprisingly nuanced problem because Python functions can
# be called in many different ways.  For example:
#
#     def func(x, y z):
#         ...
#
#     func(1, 2, 3)          # Positional arguments
#     func(x=1, y=2, z=3)    # Keyword arguments
#     func(1, z=3, y=2)      # Position/keyword argument mix
#
#     args = (1,2,3)
#     func(*args)            # Passing a tuple as positional arguments
#
#     kwargs = { 'x': 1, 'y':2, 'z': 3 }
#     func(**kwargs)         # Passing a dict as keyword arguments
#
# To make matters even more complicated, a function can force the
# use of keyword argumentss:
#
#     def func(x, *, y):
#         ...
#
#     f(1, 2)                # Error. y not supplied by keyword
#     f(1, y=2)              # Ok!
#
# Plus, there are functions that accept any number of positional
# or keyword arguments:
#
#     def func(*args, **kwargs):
#         ...
#
# -----------------------------------------------------------------------------

# Modify this function as appropriate to make it possible to call a
# function with any combination of arguments:

def after(seconds, func):
    time.sleep(seconds)
    return func()

# Show how you would call the following functions with your modified after()
# function.  A solution involving lambda is shown below.  You're allowed to
# change any part of this that you want.

# Simple function taking two arguments
def add(x, y):
    print(f'Adding {x} + {y} -> {x + y}')
    return x + y

# after(10, lambda: add(2, 3))

# Simple function taking keyword-only  arguments
def duration(*, hours, minutes, seconds):
    x = 3600*hours + 60*minutes + seconds
    print('Duration:', x)
    return x

# d = after(10, lambda: duration(hours=2, minutes=5, seconds=37))

# -----------------------------------------------------------------------------
# Exercise 4
#
# "Oh my, it's full of fail."
#
# One somewhat subtle thing about after() is that it runs a function
# on your behalf and returns its result. Carefully study and ponder
# the following two edge cases, both of which fail:
#
#     after("10", lambda: add(2, 3))      # Case 1
#     after(10, lambda: add("2", 3))      # Case 2
#
# One of these is not like the other.  But, what is different about it?
# Spend a few minutes to ponder the output and to understand what is
# happening here. Both examples result in the same kind of exception,
# but is it really the same kind of failure?
# 
# Your task: Can you redesign the after() function in a way that more
# clearly separates exception handling into two categories of
# failures--errors that are caused by bad usage of the after() function
# itself versus errors that get raised by the supplied function (func).
#
# Hint: One way to organize exceptions is to define and use a custom exception.
# -----------------------------------------------------------------------------

def after(seconds, func):
    ...

# -----------------------------------------------------------------------------
# Exercise 5
#
# The "Box".  One challenge in returning results is that there are
# actually two kinds of results from any Python function--a value
# returned by the "return" statement or an exception raised by the
# "raise" statement.  One possible design for programs that submit
# function evaluation as "work" is to place both possible results
# inside a combined Result object that gets used like this:
#
#     result = after(10, func)     # Always returns a result
# 
# Once you have the result, you "unwrap" it to get the actual outcome:
#
#   try:
#       value = result.unwrap()
#   except Exception as e:
#       print("An error occurred")
#
# Sometimes this approach is known as "boxing."  That is, the result
# gets stuffed into a box.  You don't know what it is until you open
# the box.  It's like a birthday present.
#
# Your task: Implement a Result class that allows results to be returned in
# exactly the manner as shown above.  Modify the after() function to return
# a Result instance.  
# -----------------------------------------------------------------------------

class Result:
    def unwrap(self):
        ...
        # Return the actual result or raise an exception

def after(seconds:float, func) -> Result:
    ...
    return Result(...)

# -----------------------------------------------------------------------------
# Exercise 6 - "The Chain"
#
# Although it's maybe a bit unusual in terms of Python style, one
# possibly nice thing about exercise 5 is that the after() function is
# very easy to reason about.  You give it a function as input, and it
# always returns a Result.  It doesn't raise any exceptions or return
# anything else.  That's it.
#
# However, in programming, it's also common to perform step-by-step
# sequencing of operations. For example, consider these three
# functions (type hints added to emphasize the kind of data expected):

def A(x: int) -> int:
    return x + 10

def B(x: int) -> int:
    return x * 2

def C(x:int) -> int:
    return x * x

# Now, suppose you had some code that called each function, one after the other,
# feeding the output of one function into the input of the next function.

def chained(x:int) -> int:
    a = A(x)
    b = B(a)
    c = C(b)
    return c

assert chained(2) == 576

# Or alternatively, as a single composed operation (for improved job security):

def chained(x:int) -> int:
    return C(B(A(x)))

assert chained(2) == 576

# How would this kind of chaining work if you also included the use of
# the after() function above?  For example, if you wanted to do the
# same calculation, but with time delays. Note: This is expressed as
# pseudocode--it doesn't work as shown. You'll need to modify it to
# work with the after() function in Exercise 5.

def chained_after(x:int) -> int:
    a = after(1, A(x))     # Call a = A(x) after 1 second   (must modify)
    b = after(2, B(a))     # Call b = B(a), 2 seconds after that (must modify)
    c = after(3, C(b))     # Call c = C(b), 3 seconds after that (must modify)
    return c

# assert chained_after(2) == 576        # Uncomment

# Ponder your solution code for a bit.   Can you also rewrite it as
# one-line composed operation?

#def chained_after(x):
#    return ... # everything above as a single statement
#

# -----------------------------------------------------------------------------
# Exercise 7.
#
# "The Concurrent." Although Mary has been pondering the after()
# function, it turns out that her real task is a bit more complicated.
# What she *really* wants to implement is a delayed function evaluator
# that allows other parts of the program to run while the delayed
# function works in the background.   For this, she's decided to
# use threads.   Here's an example:

import threading
def delayed(seconds, func):
    def helper():
        time.sleep(seconds)
        return func()
    threading.Thread(target=helper).start()

# If you haven't used threads before, the key idea is that a
# thread runs a function independently, and concurrently, with other
# code that happens to be running.  In the above example, the
# delayed() function returns immediately.  However, the internal
# helper() function continues to run in the background. 
#
# Here's an example, that illustrates how it works. Carefully study
# the output of running this.

def delayed_example():
    delayed(3, lambda: print("3 seconds have passed"))
    delayed(5, lambda: print("5 seconds have passed"))
    delayed(7, lambda: print("7 seconds have passed"))
    n = 10
    while n > 0:
        print('T-minus', n)
        time.sleep(1)
        n -=1
        
# Uncomment.  See what the above code produces.
# delayed_example()     

# This is all fine, but actually the problem is more complex.
# You see, Mary actually wants to be able to get a result back
# from the delayed function.  For example, something like this
# (pseudocode):

def delayed_results():
    r1 = delayed(3, lambda: add(2, 3))
    r2 = delayed(5, lambda: add(4, 5))
    f3 = delayed(7, lambda: add(6, 7))
    n = 10
    while n > 0:
        print('T-minus', n)
        time.sleep(1)
        n -=1
    print("r1=", r1)     # --> 5
    print("r2=", r2)     # --> 9
    print("r3=", r3)     # --> 13

# Your challenge:  How would you design and/or change the delayed()
# function to have it return a proper result from the delayed
# functions?   Just to be clear, those functions run in separate
# threads and allow other code to execute at the same time.
# Note: This is also a nuanced problem with many complexities.
#
# Uncomment when ready
# delayed_results()







