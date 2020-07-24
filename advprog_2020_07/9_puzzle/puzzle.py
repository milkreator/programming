# puzzle.py
#
# Objectives:
#
# In this project, we explore linguistic abstraction.  Sometimes when
# solving a problem, it makes sense to **define a domain-specific
# language**.  There are many angles on doing that in Python.  For
# instance, you can use Python itself as the language, **redefining its
# various operators** via special methods. Or you can use various
# metaprogramming features such as decorators, code inspection,
# metaclasses, etc.
#
# Consider the following logic puzzle:
#
# Baker, Cooper, Fletcher, Miller, and Smith live on different floors
# of an apartment house that contains only five floors. Baker does not
# live on the top floor. Cooper does not live on the bottom
# floor. Fletcher does not live on either the top or the bottom
# floor. Miller lives on a higher floor than does Cooper. Smith does
# not live on a floor adjacent to Fletcher's. Fletcher does not live on
# a floor adjacent to Cooper's. Where does everyone live?

# -----------------------------------------------------------------------------
# Exercise 1 - Brute force
#
# Write a program that finds a solution to the problem.  The program
# should output the floor on which each person lives.
#
# To do this, think about a brute force solution. You know that Baker,
# Cooper, Fletcher, Miller, and Smith all live on different floors
# of an apartment.  One way to solve it would be to cycle through
# all permutations of the floors and to enforce the various rules
# as a series of constraints.
# -----------------------------------------------------------------------------

def unique(*items):
    return len(items) == len(set(items))

def brute_force():
    for baker in range(1,6):
        for cooper in range(1,6):
            for fletcher in range(1,6):
                for miller in range(1,6):
                    for smith in range(1,6):
                        # now enfore the constraints
                        if not unique(baker, cooper, fletcher, miller, smith):
                            continue
                        if baker == 5:
                            continue
                        if cooper == 1:
                            continue
                        if fletcher == 5 or fletcher == 1:
                            continue
                        if miller < cooper:
                            continue
                        if abs(smith - fletcher) == 1:
                            continue
                        if abs(fletcher - cooper)  == 1:
                            continue
                        else:
                            print(f'baker={baker},cooper={cooper},fletcher={fletcher},miller={miller},smith={smith}')


brute_force()

# -----------------------------------------------------------------------------
# Exercise 2 - Bending the rules
#
# Sometimes when faced with a **complicated problem domain**, it makes sense
# to abstract things into a kind of **domain-specific language**.  For example,
# one way to express the above logic puzzle is as **a series of definitions
# and constraints**:
#
#    # Definitions of possible values
#    baker = {1, 2, 3, 4, 5}
#    cooper = {1, 2, 3, 4, 5}
#    fletcher = {1, 2, 3, 4, 5}
#    miller = {1, 2, 3, 4, 5}
#    smith = {1, 2, 3, 4, 5}
#
#    # -- Constraints
#    require(distinct(baker, cooper, fletcher, miller, smith))
#    require(baker != 5)
#    require(cooper != 1)
#    require(fletcher != 1 and fletcher != 5)
#    require(miller > cooper)
#    require(abs(smith-fletcher) > 1)
#    require(abs(fletcher-cooper) > 1)
#
# Python has a wide range of **metaprogramming** features (e.g.,
# decorators, metaclasses, etc.) that allow you to change the way that
# functions and classes work.  Sometimes these features can be used
# to bend the rules a bit--or a lot.
#
# That's your challenge in this exercise: Can you implement a logic
# puzzle solver in the form a function decorator?  Like this:
#
# @solver
# def multi_dwelling(baker, cooper, fletcher, miller, smith):
#     require(distinct(baker, cooper, fletcher, miller, smith))
#     require(baker != 5)
#     require(cooper != 1)
#     require(fletcher != 1 and fletcher != 5)
#     require(miller > cooper)
#     require(abs(smith-fletcher) > 1)
#     require(abs(fletcher-cooper) > 1)
#     print(f'Solution: {baker=} {cooper=} {fletcher=} {miller=} {smith=}')
#
# multi_dwelling(
#     baker={1, 2, 3, 4, 5},
#     cooper={1, 2, 3, 4, 5},
#     fletcher={1, 2, 3, 4, 5},
#     miller={1, 2, 3, 4, 5},
#     smith={1, 2, 3, 4, 5}
# )
#
# The basic idea is that you just call the function with arguments set
# to the possible values and it magically finds a solution if there is
# one.  The specific solution is passed in as the actual function
# arguments. If no solution can be found, an exception should be
# raised.
#
# Note: To do this, you'll need to implement the @solver decorator along
# with supporting functions such as require() and distinct()
# -----------------------------------------------------------------------------
class Fail(Exception):
    pass

def require(test):
    if not test:
        raise Fail()  # this wil lsignal the solver to move onto the next test case

def distinct(*items):
    return len(items)  == len(set(items))

#import itertools
def all_candidates(kwargs):
    # input like this
    # {  baker: {1,2,3,4,5},
    #    miller: {1,2,3,4,5},
    #    ...
    #  }
    #
    #  vals is 
    import itertools
    for vals in itertools.product(*kwargs.values()):  # vals is a tuple like (1, 2,2, 1,4) (some combination of values)
        yield dict(zip(kwargs, vals))   # a dict like {'baker': 1, 'miller':2, ... }

def solver(func):
    def search(**kwargs):
        for candidate in all_candidates(kwargs):
            try:
                func(**candidate)
            except Fail:
                pass
    return search


@solver
def multi_dwelling(baker, cooper, fletcher, miller, smith):
    require(distinct(baker, smith, fletcher, cooper, miller))
    require(baker != 5)
    require(cooper != 1)
    require(fletcher != 1 and fletcher != 5)
    require(miller > cooper)
    require(abs(smith-fletcher) > 1)
    require(abs(fletcher-cooper) > 1)
    print(f'baker={baker},cooper={cooper},fletcher={fletcher},miller={miller},smith={smith}')

multi_dwelling(
    baker = {1, 2, 3, 4,5},
    smith = {1, 2, 3, 4,5},
    fletcher = {1, 2, 3, 4,5},
    cooper = {1, 2, 3, 4,5},
    miller = {1, 2, 3, 4,5}
)



"""
    # specify the domain for certain values

"""


# -----------------------------------------------------------------------------
# Exercise 3 - Liars
#
# Using your decorator, see if you can solve the "Liars Problem":
#
# Five schoolgirls sat for an examination. Their parents--so they
# thought--showed an undue degree of interest in the result. They
# therefore agreed that, in writing home about the examination, each
# girl should make one true statement and one untrue one. The following
# are the relevant passages from their letters:
#
# Betty: "Kitty was second in the examination. I was only third."
# Ethel: "You'll be glad to hear that I was on top. Joan was second."
# Joan: "I was third, and poor old Ethel was bottom."
# Kitty: "I came out second. Mary was only fourth."
# Mary: "I was fourth. Top place was taken by Betty."
#
# What, in fact, was the order in which the five girls were placed?
# -----------------------------------------------------------------------------




# -----------------------------------------------------------------------------
# Exercise 4 - A Problem Class
#
# Sometimes classes can be used to define domain-specific problems.
# Can you recast your solver to work with code similar to the following?
#
# class MultiDwelling(Problem):
#    # Definitions of possible values
#    baker = {1, 2, 3, 4, 5}
#    cooper = {1, 2, 3, 4, 5}
#    fletcher = {1, 2, 3, 4, 5}
#    miller = {1, 2, 3, 4, 5}
#    smith = {1, 2, 3, 4, 5}
#
#    # -- Constraints
#    require(distinct(baker, cooper, fletcher, miller, smith))
#    require(baker != 5)
#    require(cooper != 1)
#    require(fletcher != 1 and fletcher != 5)
#    require(miller > cooper)
#    require(abs(smith-fletcher) > 1)
#    require(abs(fletcher-cooper) > 1)
#
# solns = MultiDwelling.solutions()     # Return all solutions


# idea
# use doc-strings  
class Puzzle:
    @classmethod
    def __init_subclass__(cls):
        print("DO SOMTEHING")
        print(cls.__doc__)   # look at the doc string

class DwellingProblem(Puzzle):
    ...