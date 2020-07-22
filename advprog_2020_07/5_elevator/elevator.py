# -----------------------------------------------------------------------------
# elevator.py
#
# Certain problems often involve the implementation of **"state
# machines."**  For example, consider the operation of an elevator.  At
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
# information means that **your implementation will need to be
# extended/embedded in some other software** (not shown/provided) to be
# used in the real world.  It also means that your understanding
# of the problem might be incomplete--you should write the code
# in anticipation of new unforeseen "requirements."
# -----------------------------------------------------------------------------

# A Hint: It might make sense to **separate the problem into separate
# concerns**.  For example, perhaps you define an "Elevator" class that
# deals with the logic of the elevator and a "ElevatorControl" class
# that is focused on its interaction with "real" world elements.  For
# example:

class Elevator:
    # Logic of the elevator

    # make the __init__ function **take default args** for all elements of
    # internal state. useful for later testing. 
    #  for a very specific state. and then exectue an envent and watch what happens
    def  __init__(self, mode='IDLE', floor = 1, final_floor = None, 
                        direction = None, destinations=None,
                        up_requests = None, down_requests=None):
        self.mode = mode if mode else IdleMode     # {IDLE, MOVING, LOADING}
        self. floor = floor
        self.final_floor = final_floor             # current floor
        #self.direction = direction
        self.destinations = set()  if destinations is None else destinations # ALL DESTINATION BUTTONS PRESSED
        self.up_requests = set() if up_requests is None else up_requests
        self.down_requests = set() if down_requests is None else down_requests

    # define a useful __repr__() method so that you can look at it with print() and for debugging
    def __repr__(self):
        return f'Elevator({self.mode}, {self.floor}, {self.final_floor}, {sorted(self.destinations)},\
        {sorted(self.up_requests)}, {sorted(self.down_requests)})'
   
    def update_final_floor(self, floor_request):
        # if no final floor, we'll just assign it to the new request.
        if self.final_floor is None:
            self.final_floor = floor_request

        # if elevator is below it's final floor and an even higher floor request
        # arrrive, update
        if self.floor < self.final_floor and floor_request > self.final_floor:
            self.final_floor = floor_request

        # if elevator is above its final floor and an even lower floor request
        # arrives, make that the final floor
        elif self.floor > self.final_floor and floor_request < self.final_floor:
            self.final_floor = floor_request

    def engage_motor(self, control):
        if self.final_floor > self.floor:
            control.hoist_motor('up')
            self.mdoe = MovingMode
        elif self.final_floor < self.floor:
            control.hoist_motor('down')
            self.mode = MovingMode
        else:
            self.mode = IdleMode

    
    # define "event handler" methods 
    def down_button_pressed(self, floor, control):
        self.mode.down_button_pressed(self, floor, control)
    
    def up_button_pressed(self, floor, control):
        self.mode.up_button_pressed(self, floor, control)

    def destination_button_pressed(self, floor, control):
        self.mode.destination_button_pressed(self, floor, control)

    def floor_sensor(self, floor, control):
        self.mode.floor_sensor(self, floor, control)

    def timer_expired(self):
        self.mode.time_expired(self, floor, control)
        #raise RuntimeError("should not happen")

# customer defined
# # Operational mode classes.  You implement the logic for each event.
# operational mode classes, the elev arg here is actually the Elevator instance above

_events = ['down_button_pressed', 'up_button_pressed']

class ModeBase:
    @classmethod
    def __init_subclass__(cls):
        for name in _events:
            assert hasattr(cls, name), f'{name} event not handled'

class IdleMode:
    def down_button_pressed(elev, floor, control):
        # someone pressed a  "down" button in the hallway
        
        if floor == elev.floor:
            # the elevator is already on the floor. open the door and load
            control.door_control("open")
            control.set_time(10)
            elev.mode = LoadingMode
            #self.door_requests.discard(floor)
        else:
            elev.down_requests.add(floor)
            elev.update_final_floor(floor)
            elev.engage_motor(control)
            #elev.mode = MovingMode

    def up_button_pressed(elev, floor, control):
        if floor == elev.floor:
            control.door_control('open')
            control.set_timer(10)
            elev.mode = LoadingMode
        else:
            elev.up_requests.add(floor)
            elev.update_final_floor(floor)
            elev.engage_motor(control)

    def destination_button_pressed(elev, floor, control):
        if floor == elev.floor:
            control.door_control('open')
            control.set_timer(10)
            elev.mode = LoadingMode
        else:
            elev.destinations.add(floor)
            elev.update_final_floor(floor)
            elev.engage_motor(control)
    
    def floor_sensor(elev, floor, control):
        raise RuntimeError("Should not happen")
   
    def timer_expired(elev):
        raise RuntimeError("should not happen")
    

class MovingMode:
    def down_button_pressed(elev, floor, control):
        elev.down_requests.add(floor)
        elev.update_final_floor(floor)

    def up_button_pressed(elev, floor, control):
        ...

class LoadingMode:
    ...


# old code
if 0:
    def down_button_pressed(self,  floor, control):
        # someone pressed a  "down" button in the hallway
        self.down_requests.add(floor)

        if self.mode == "IDLE":
            if floor == self.floor:
                # the elevator is already on the floor. open the door and load
                control.door_control("open")
                control.set_time(10)
                self.mode = 'LOADING'
                #self.door_requests.discard(floor)
            else:
                self.update_final_floor(floor)
                self.engage_motor(control)
                self.mode = 'MOVING'
            """
            elif floor > self.floor:
                control.hoist_motor("up")
                self.mode = 'MOVING'
            elif floor < self.floor:
                control.hoist_motor("down")
                self.mode = 'MOVING'
            """

    def up_button_pressed(self, floor, control):
        # someone pressed a  "up" button in the hallway
        self.up_requests.add(floor)
        ...


    def destination_button_pressed(self, floor, control):
        # someone pressed a button inside the elevator  
        # Figure out what to do next
        self.destinations.add(floor)

        if self.mode == "IDLE":
            ...
        elif self.mode == 'MOVING':
            ...
        elif self.mode == 'LOADING':
            ...
             
        # Issue a control command
        control.hoist_motor("up")

    def timer_expired(self):
        #timer that expires  after the doors have been open for a while
        if self.mode == 'LOADING':
            ...
        else:
            # the timer is only used to keep the doors open when loading
            raise RuntimeError("should not happen")
        

    def floor_sensor(self, floor):
        # sensor in the elevator shaft to indicate the elevator is at a certain floor
        if self.mode == 'MOVING':
            ...
        else:
            # floor sensors are only tripped while elevator is in motion. 
            # should not happen if elevator is idle or wrong 
            raise RuntimeError("should not happen")



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

    @abstractmethod
    def set_timer(self, timer):
        pass


class DebugElevatorControl(ElevatorControl):
    def hoist_motor(self, command):
        print("hoist_motor:", command)

    def door_control(self, command):
        print("door_contorl:", command)
        
    def set_timer(self, seconds):
        print("set_timer:", seconds)


class MockElevatorControl(ElevatorControl):
    def __init__(self, motor_state='off', door_state='closed', timer=None):
        self.motor_state = motor_state
        self.door_state = door_state
        self.timer = timer
        #self.commands = []
    
    def __repr__(self):
        return f'MockElevatorControl({self.motor_state}, {self.door_state}, {self.timer})'

    def invariants(self):
        assert not (self.door_state == 'open' and self.motor_state != 'off')

    def hoist_motor(self, command):
        #self.commands.append(('hoist', command)) 
        assert command in {'up', 'down', 'off'}
        self.motor_state = command
        self.invariants()

    def door_control(self, command):
        #self.commands.append(('door', command)) 
        assert command in {'open', 'close'}
        self.door_state= command
        self.invariants()

    def set_timer(self, seconds):
        #self.commands.append(('timer', seconds))  
        assert seconds is None or seconds > 0
        self.timer = seconds

# Unit Test
def test_idle_move():
    # logic ->  the logic of the elevator 
    elev = Elevator(mode=IdleMode, floor=1)
    # controller -> focused on its interaction with "real" world elements 
    control = MockElevatorControl()
    # 
    elev.down_button_pressed(3, control)
    # assert control.commands == [('hoist', 'up')]
    assert control.motor_state == 'up'
    assert elev.mode == MovingMode
    assert 3 in elev.down_requests  

test_idle_move()

# -----------------------------------------------------------------------------
# The Testing Challenge - verify 
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

#  verify
#elev = Elevator()
#control = MockElevatorControl()

def next_elevators(elev, control:MockElevatorControl):
    # Idea .
    # Given an elevator and controller, figure out every possible "next"
    # elevator that you could have

    # think about events ... what events could happen  

    # 1. destination buttons inside the elevator
    for floor in range(1,6):
        elev.destination_button_press(floor, control)

    # 2. up requests get pressed
    for floor in range(1,5):
        elev.up_button_press(floor, control)

    # 3. down requests get pressed

    # 4. if the controller motor is on, could floor sensor trip

    # 5. if a timer is set, it could expire
    if control.timer is not None:
        elev.timer_expired(control)


def simulate():
    init = Elevator()
    control = MockElevatorControl()

    ...