# message.py
#
# Introduction
# ------------
# Arjoon is working on a distributed system involving message passing.
# There are several components to the system including messages,
# dispatching, and message encoding.  However, our concern here is not
# so much the actual mechanics of the messaging (i.e., networks), but
# issues related to **the organization and composition of the parts**
# that will ultimately make up the system.

# -----------------------------------------------------------------------------
# Exercise 1 - This message will self destruct... maybe
#
# In this messaging system, programs potentially run forever, creating
# billions of messages.  One area of concern is **object management and
# garbage collection**. When do messages get destroyed?  Is it possible
# for Python to leak memory?  Is it going to be one of those programs
# you have to "restart" every so often simply to clean up?
#
# Python uses **reference counting** to manage the life-time of objects.
# The reference count is increased on an object whenever you make a
# new variable reference or store it in any kind of container.  The
# reference count is decreased when variables go away or the object is
# removed from a container.  Normally, it just "works" and you don't
# worry about it.
#
# The __del__() method, if defined on an object, is called when the
# reference count of an object has reached zero and it's about to be
# destroyed.  It's rarely necessary to define this, but doing so can
# be instructive to learn more about how Python works.
#
# Consider the following Message class. A message consists of a source
# and destination address. An internal, always incrementing, sequence
# number is also attached to it.

class Message:
    _sequence = 0

    def __init__(self, source, dest,  payload=None, _sequence = None):
        self.source = source
        self.dest = dest
        #self.signature = signature
        self.payload = payload
        if _sequence is None:
            self.sequence = Message._sequence
            Message._sequence += 1
        else:
            self.sequence = _sequence

    def __repr__(self):
        return f'Message<{self.sequence}: source={self.source}, dest={self.dest}>'

    def __del__(self):
        print(f'Message {self.sequence} destroyed')

# Try an interactive example of creating and destroying a message.
#   
#    >>> m = Message(0, 1)
#    >>> del m
#    Message 0 destroyed
#    >>>
# 
# YOUR CHALLENGE: See if you can find a "normal" coding scenario where
# a Message is created, used, and all obvious references to the
# message then seem to go away, but the message is NOT immediately
# destroyed.  Note: by "normal", I mean code that uses a Message in a
# typical message-like way--not something weird like intentionally
# creating recursive messages or message reference cycles.
#
# Note: Don't spend too much time on this--you might not be able to find
# a scenario where memory is leaked.  That's good!  We don't want
# our program to leak memory.
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Exercise 2 - The Game
#
# Suppose that this messaging system was going to be used to implement
# a game and there different types of game messages--each holding different
# information (i.e., chat messages, player updates, player actions,
# etc.).  For example (in psuedocode):
#
#    ChatMessage {
#        player_id : int    # Player id sending message
#        text : str         # Message contents (UTF-8 Text)
#    }
#
#    PlayerUpdate {
#        player_id : int    # Player being updated
#        x : float          # New x position
#        y : float          # New y position
#    }
#
# How would you implement these different message types in this system
# and how would your implementation relate to the Message class above.
# Define the Python classes for the above messages.
# -----------------------------------------------------------------------------

#proposal 1: Inherit from message
class _ChatMessage(Message): # tight coupling
    # **cannot change the Message inor butf if you donot know the Message**
    def __init__(self, source, dest,  player_id, text):
        super().__init__(source, dest)
        #self.message = Message(source, dest)
        self.player_id = player_id
        self.text = text

msg1 = _ChatMessage(0, 1, 123, "Hello World")


class ChatMessage:
    def __init__(self, player_id, text):
        self.player_id = player_id
        self.text = text

msg1 = Message(0,1, ChatMessage(123, "Hello World"))

# proposal 2: Embed inside Message
class PlayerUpdate:  # <<< Does not inherit from Message
    def __init__(self, player_id, x, y):
        self.player_id = player_id
        self.x = x
        self.y = y

msg2 = Message(0, 1, PlayerUpdate(123, 10,20))

# question: pick one ... why?
# option2,  allows classes to vary independently
# option1, less plumbing (maybe simpler)

# -----------------------------------------------------------------------------
# Exercise 3 - Message on a Wire
#
# In order to send a message someplace, it needs to be serialized into
# a stream of bytes and deserialized from bytes back into a Message
# instance.  Assume that there's supposed to be some kind of "encode"
# operation that takes a Message and turns it into bytes and a
# "decode" operation takes bytes and turns them back into a Message.
#
# Design Challenge: How would you structure/write code to handle the
# message encoding/decoding problem with the following design
# considerations:
#
# - There are might be hundreds of different game message types, each
#   with different data fields
# - There are many possible low-level message encodings (pickle, 
#   JSON, XML, etc.).  These encodings might be hooked to other
#   programming languages.  They might involve binary data. They
#   might NOT be Python-specific (like Pickle) or based on passing
#   dictionaries around (like JSON). 
# - It might be necessary to implement a new encoding in the future.
#
# Note: This is a fairly open-ended problem that is fraught with peril.
# -----------------------------------------------------------------------------

from abc import ABC, abstractmethod
class MessageCodec(ABC):
    @abstractmethod
    def encode(self, msg: Message) -> bytes:
        pass
    
    @abstractmethod
    def decode(self, data: bytes) -> Message:
        pass

#
import pickle
class PickleCodec(MessageCodec):
    def encode(self, msg):
        return pickle.dumps(msg)
    
    def decode(self, data):
        return pickle.loads(data)

import json
class JSONCodec(MessageCodec):
    def encode(self, msg):
        # convert msg into dict
        d = dict(msg.__dict__)
        d['playload'] = dict(msg.payload.__dict__)
        d['payload_type'] = type(msg.payload.__name__)
        return json.dumps(d).encode('utf-8')
        
    def decode(self, data):
        d = json.loads(data.decode('utf-8'))
        payload_type= d.pop('payload_type')
        payload = d['payload']
        ...

# The following "test" illustrates the basic requirements of encoding/decoding
def test_serial():
    #m1 = ChatMessage(0, 1, 123, "Test Message")  # This might vary depending on (2) above
    m1 = Message(0, 1, ChatMessage(123, "Test Message"))

    codec = PickleCodec()
    # You need to figure out the "encode" operation.  It can look different
    # than what's shown, but the final result must be bytes.
    raw = codec.encode(m1)

    # The encoded message (whatever it is) must be bytes. Something that
    # can be transmitted somewhere else.
    assert isinstance(raw, bytes)

    # The decode operation must accept bytes and recreate a message.
    # Again, this can look different than what's shown.  However, the
    # final result must be identical to the original message.
    m2 = codec.decode(raw)

    # The final message must be identical to the original message in
    # every way.  This includes the dest, source, sequence numbers,
    # payload, and everything The following assert verifies this by
    # running the two messages above (m1 and m2) through pickle. The
    # resulting byte sequences should be identical.
    import pickle
    assert pickle.dumps(m1) == pickle.dumps(m2)

# Uncomment
test_serial()

# -----------------------------------------------------------------------------
# Exercise 4 - There can be only one
#
# To send messages, Arjoon has decided on an architecture where all
# messages are given to a central Dispatcher object. Its primary
# method is send().  You provide a message to the Dispatcher and it
# takes care of delivering it to a proper location.
#
# The actual implementation details of the Dispatcher delivery process
# are left somewhat vague. This is by design.  Yes, there is a send()
# method, but the internal implementation of could be almost anything.
# We just don't know.  We're not really supposed to know.  It's like
# the post office--you drop off a letter and what happens beyond that
# is not our problem.
#
# With that in mind, here is a new problem involving the Dispatcher.
#
# 1. An instance of some kind of Dispatcher class must 
#    be created in the application.  
#   
# 2. That instance must implement the required send() method.
#
# 3. There can only be ONE instance of a Dispatcher object created 
#    in the entire program (i.e., a "Singleton")
#
# 4. There must be some way for code to easily obtain a reference 
#    to the ONE Dispatcher instance. 
#
# Your challenge: Implement this.
# -----------------------------------------------------------------------------

from abc import ABC, abstractmethod

class Dispatcher(ABC):
    '''
    Base class.  Do not create instances of this. Use a subclass.
    '''
    _the_dispatcher = None   # the one dispatcher instance
    @abstractmethod
    def send(self, msg):
        pass

def get_dispatcher():
    return Dispatcher._the_dispatcher

def register_dispatcher(dispatcher):
    assert Dispatcher._the_dispatcher is None, "Dispatcher already set"
    Dispatcher._the_dispatcher = dispatcher

# Example of a child-class that simply prints messages.
class SimpleDispatcher(Dispatcher):
    def send(self, msg):
        print('Sending:', msg)

# Example: must take place in application startup/configuration
register_dispatcher(SimpleDispatcher())

# There must be some way to obtain/access the dispatcher object from 
# any other code. Is getting the dispatcher the same as creating one?
# What is the programming interface for this?
def test_send():
    d = get_dispatcher()     # get the one true dispatcher somehow
    d.send("Hello World")   # Send a message of some sort

# Uncomment
test_send()

# Thought:  How do you ensure that there is only one Dispatcher?

# -----------------------------------------------------------------------------
# Exercise 5 - The Unsubscribe Problem
#
# Arjoon has decided to implement a dispatcher based on the idea of
# publish/subscribe.  The general idea is that different handlers can
# subscribe to a specific message destination address. Any message
# sent to that address will be given to the handler.  If multiple
# handlers are subscribed to the same address, each handler will
# receive all of the messages.  Here's an example of a Dispatcher that
# implements this general idea.

from collections import defaultdict

class PubSubDispatcher:
    def __init__(self):
        self.subscribers = defaultdict(set)

    def subscribe(self, addr, handler):
        self.subscribers[addr].add(handler)

    def send(self, msg):
        for handler in self.subscribers[msg.dest]:
            handler.receive_message(msg)

# An example of of handler that receives messages
class ExampleHandler:
    def __init__(self, name):
        self.name = name

    def receive_message(self, msg):
        print(f'{self.name} got', msg)

# An example of using using the dispatcher and subscribing a handler
def pubsub_example():
    dispatcher = PubSubDispatcher()
    # Create some handlers
    h1 = ExampleHandler("Handler1")
    h2 = ExampleHandler("Handler2")
    dispatcher.subscribe(0, h1)       # h1 subscribed to channel 0
    dispatcher.subscribe(1, h2)       # h2 subscribed to channel 1
    dispatcher.subscribe(1, h1)       # h1 additionally subscribed to channel 1
    dispatcher.send(Message(0, 1))    # Message from 0 -> 1   
    dispatcher.send(Message(1, 0))    # Message from 1 -> 0

# Uncomment to try it.  Make sure you understand what's happening above.
# pubsub_example()

# THE DEBATE:
# ===========
#
# The above dispatcher is simple enough, but a debate has erupted over
# the proper way to *unsubscribe* handlers from the
# dispatcher. Basically, the problem relates to the lifetime of the
# handler objects themselves.  When no longer needed, it should be
# possible to detach the handler from the dispatcher in some way.
#
# Option 1:  Explicit Unsubscribe.
# --------------------------------
# Arjoon thinks that a simple solution to this problem is to implement
# an explicit "unsubscribe()" method that takes the same arguments
# as subscribe().  You use it like this:
#
#     dispatcher.subscribe(channel, handler)
#     ...
#     dispatcher.unsubscribe(channel, handler)
#
# "It's straightforward. It's easy", he argues.
#
# Option 2:  Unsubscribe on Garbage Collection
# --------------------------------------------
# Mel thinks that handlers should automatically unsubscribe themselves
# when they go out of scope and are garbage collected.  She's proposed
# a different kind of function "watch()" that works like this:
#
#      handler = ExampleHandler()
#      dispatcher.watch(channel, handler)
#      ...
#      del handler         # Handler is automatically unsubscribed.
#
# "You don't have to worry about it", she argues.
#
# Option 3: Unsubscribe with a Context Manager
# --------------------------------------------
# Python supports a feature known as a "context manager" that's
# often used to define a scope/lifetime in which an object is used.
# You've used it if you've ever used the "with" statement in
# combination with a file, a lock, or some other resource.
#
# Michelle thinks that all of this could be refined by introducing the
# idea of a dispatcher context.  You'd use it like this:
#
#     with dispatcher as context:
#         handler = ExampleHandler()
#         context.subscribe(channel, handler)
#         ...
#     # All handlers in the context automatically unsubscribed
#
# YOUR CHALLENGE:
# ---------------
# Modify the PubSubDispatcher class so that it supports *ALL THREE* of
# the above subscribe/unsubscribe approaches.
#
# The following tests will verify that it's working.  Note: You
# should be able to pass all three tests at once.

class TestHandler:
    def __init__(self, name, maxuse):
        self.name = name
        self.maxuse = maxuse
        
    def receive_message(self, msg):
        assert self.maxuse > 0, "Why did I receive this?"
        print(f'{self.name} got', msg)
        self.maxuse -= 1

# Option 1: Explicit unsubscribe
def test_option1():
    dispatcher = PubSubDispatcher()
    h1 = TestHandler("Handler1", 1)
    dispatcher.subscribe(1, h1)
    dispatcher.send(Message(0, 1))
    dispatcher.unsubscribe(1, h1)
    dispatcher.send(Message(0, 1))    # Handler should not receive this
    print("Good unsubscribe")

# test_option1()            # Uncomment

# Option 2:
def test_option2():
    dispatcher = PubSubDispatcher()
    h2 = TestHandler("Handler2", 1)
    dispatcher.watch(1, h2)
    dispatcher.send(Message(0, 1))
    del h2
    dispatcher.send(Message(0, 1))    # Handler should not receive
    print("Good watching")

# test_option2()           # Uncomment

# Option 3:
def test_option3():
    dispatcher = PubSubDispatcher()
    with dispatcher as context:
        h2 = TestHandler("Handler3", 1)
        context.subscribe(1, h2)
        dispatcher.send(Message(0, 1))
        
    dispatcher.send(Message(0, 1))    # Handler should not receive
    print("Good context manager")

# test_option3()          # Uncomment

    
        
    
