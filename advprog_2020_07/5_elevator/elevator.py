# -----------------------------------------------------------------------------
# elevator.py
#
# Certain problems often involve the implementation of "state
# machines."  For example, consider the operation of an elevator.  At
# any given moment, the elevator is in a certain "operational state".
# For example, it's positioned at a given floor and it's either
# idle, loading passengers, or moving. The doors are open or closed.
# The elevator transitions between states according to various events
# which may include buttons, sensors, and timers.
#
# Suppose that you are tasked with designing and writing the control
# software for an elevator in a 5-floor building.   The elevator has
# the following inputs:
#
#  1. A push button inside the elevator to select a destination floor.
#  2. Two push buttons (up/down) on each floor to request the elevator.
#  3. A sensor on each floor to indicate the current elevator position 
#     (triggered when the elevator reaches a given floor).
#  4. A time-expired event that's used for time-related operation.
#
# The elevator has the following control outputs:
#
#  1. Hoist motor control (controls up/down motion)
#  2. Door motor control (controls door open/close motion)
#  3. Set a timer.
#
# The elevator operates in three primary operational modes.
#
# 1. IDLE: The elevator remains still if there are no floor requests.  
#    This means it's just stopped on whatever floor it happened to
#    go to last with the doors closed.  Any request causes
#    the elevator to start moving towards that floor.
#    
# 2. MOVING: The elevator is in motion. Once in motion, the
#    elevator continues to move in its current direction until
#    it reaches the highest or lowest requested floor.  Along
#    the way, the elevator will serve other requests as appropriate.
#    For example, suppose the elevator is on floor 1 and someone
#    hits the "down" button on floor 4.  The elevator will start
#    moving up.  If, on the way up, someone presses "up" on 
#    floor 3, the elevator will stop and load passengers before
#    continuing up to floor 4.  If someone also pressed "down" on
#    floor 5, the elevator would *pass* floor 4 and go up to
#    floor 5 first.  It would then stop on floor 4 on its way
#    back down. 
#
# 3. LOADING: When stopped at a floor, the door opens for 10 seconds
#    and then closes again.  There is no mechanism to make the door
#    stay open.  Anything in the way gets cut in half--an obvious
#    limitation to be addressed in a future version.
#
# YOUR TASK: Design and implement code for the internal logic and
# control of the elevator.  Come up with some strategy for testing it.
#
# CHALLENGE: To write this code you might ask to know more about how
# the elevator control actually works (i.e., How are inputs delivered?
# How is data encoded?  How are commands issued to the motors?). How
# does the elevator deal with acceleration and deceleration. However,
# you're not going to get it. That's a different corporate division.
# So, you've got to figure out how to implement the elevator control
# software without any first-hand knowledge of its deployment
# environment or the laws of physics.  Naturally, the lack of
# information means that your implementation will need to be
# extended/embedded in some other software (not shown/provided) to be
# used in the real world.  It also means that your understanding
# of the problem might be incomplete--you should write the code
# in anticipation of new unforeseen "requirements."
# -----------------------------------------------------------------------------

# A Hint: It might make sense to separate the problem into separate
# concerns.  For example, perhaps you define an "Elevator" class that
# deals with the logic of the elevator and a "ElevatorControl" class
# that is focused on its interaction with "real" world elements.  For
# example:

class Elevator:
    # Logic of the elevator
    def destination_button_pressed(self, floor, control):
        # Figure out what to do next
        ...  
        ...        
        # Issue a control command
        control.hoist_motor("up")

from abc import ABC, abstractmethod

# Abstract base class for implementing "elevator" commands. Must
# be subclassed and implemented for the real elevator (details unknown).
class ElevatorControl(ABC):
    @abstractmethod
    def hoist_motor(self, command):
        pass

    @abstractmethod
    def door_control(self, command):
        pass


# -----------------------------------------------------------------------------
# The Testing Challenge
#
# One issue with the elevator software is the problem of testing it.
# Yes, you can probably write some unit tests for selected parts of
# your state machine.  However, can you be sure that you've tested
# every possible scenario of events?  Also, just what kinds of things
# can go wrong with an elevator anyways?
#
# In answering that last question, there are probably a few obvious
# "safety" issues you could envision. For example, the elevator should
# probably never move with the doors open.  Likewise, it probably
# shouldn't try to move up when already on the top floor (or down when
# at the bottom).  Other kinds of problems are more subtle.  For
# instance, you probably wouldn't want the elevator software to
# deadlock (i.e., just freeze with nothing happening at all).  Or have
# a situation where kids on two floors could launch a denial of
# service attack on the elevator by constantly pressing buttons and
# making the elevator ping-pong back and forth between just those
# floors.
# 
# One way to explore this space is to write a elevator simulator.
# Think of it as the "Game of Elevator."  The game starts with the
# elevator in some starting state.  From that starting state, any
# event could happen (i.e., any button could be pressed).  Each of
# these cause the elevator to change to a new state.  From all of
# these new states, you repeat the process to get more states and so
# on.  It's like exploring all possible moves that could occur in a
# board game.  Can you write something like this for the elevator?
# That is, can you write a simulation that runs the elevator software
# through every possible combination of runtime state, checking for
# potential problems?  This is your mission, should you choose to
# accept it.
#


