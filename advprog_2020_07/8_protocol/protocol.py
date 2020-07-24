# protocol.py
#
# Objective:
# ----------
# Learn a bit about I/O handling, the implementation of I/O protocols,
# and the challenges of programming in a post-async environment.
#
# Introduction:
# -------------
# Arjoon, in implementing his Distributed Messaging System from
# project 4 is now focused on the problem of actually sending messages
# over network connections.  He has decided that each message will be
# encoded according to the following scheme:
#
# 1. The message type will be encoded as a UTF-8 string, terminated by
#    a newline (\r\n).
#
# 2. The message size (an integer) will be encoded as a UTF-8 string,
#    terminated by a newline (\r\n).
#
# 3. The message contents, encoded as UTF-8 JSON will follow.
#
# To illustrate, suppose that the following classes represent a few
# different kinds of messages:

class Message:
    _sequence = 0
    def __init__(self):
        Message._sequence += 1
        self.sequence = Message._sequence

class ChatMessage(Message):
    def __init__(self, playerid, text):
        super().__init__()
        self.playerid = playerid
        self.text = text

class PlayerUpdate(Message):
    def __init__(self, playerid, x, y):
        super().__init__()
        self.playerid = playerid
        self.x = x
        self.y = y

# Here's how to encode a message according to the above protocol
def encode_message(msg):
    import json
    msgtype = type(msg).__name__.encode('utf-8') + b'\r\n'
    payload = json.dumps(msg.__dict__).encode('utf-8')
    size = str(len(payload)).encode('utf-8') + b'\r\n'
    return msgtype + size + payload

# An example that shows the encoding for a few messages
def example():
    msg1 = ChatMessage('Dave', 'Hello World')
    msg2 = PlayerUpdate('Paula', 23, 41)
    print(encode_message(msg1))
    print(encode_message(msg2))

example()

# -----------------------------------------------------------------------------
# Exercise 1 - The recreator
#
# Taking a message and turning it into bytes is straightforward.  However,
# how do you actually get a message back?
#
# Your first task is to write a message creation function that takes
# the name of message type and the JSON-encoded payload (as text) and
# turns it back into a proper Python object.  The function should
# raise an exception if the specified message type doesn't correspond
# a valid message definition.
#
# Bonus: Could you also make the function enforce the presence of required
# message attributes?
import json

def recreate_message(msgtype, payload):
    # You implement
    data = json.loads(payload)
    sequence = data.pop('sequence')
    if msgtype == 'ChatMessage':
        msg = ChatMessage(**data)
    elif msgtype == 'PlayerUpdate':
        msg = PlayerUpdate(**data)
    else:
        raise RuntimeError('Bad message type')

    # retroactively patch the sequence number
    msg.sequence = sequence
    return msg


def test_recreator():
    msg1 = recreate_message('ChatMessage', '{"sequence": 1, "playerid": "Dave", "text": "Hello World"}')
    assert isinstance(msg1, ChatMessage) and \
           msg1.sequence == 1 and \
           msg1.playerid == 'Dave' and \
           msg1.text == 'Hello World'

    msg2 = recreate_message('PlayerUpdate', '{"sequence": 2, "playerid": "Paula", "x": 23, "y": 41}')
    assert isinstance(msg2, PlayerUpdate) and \
        msg2.sequence == 2 and \
        msg2.playerid == 'Paula' and \
        msg2.x == 23 and \
        msg2.y == 41

    print("Ok creator.")

    try:
        msg3 = recreate_message('HackerMsg', '{"x": 666}')
        assert False, "Why did this work?!?!?! Bad creator!"
    except Exception as e:
        print("Good creator!")

    try:
        msg4 = recreate_message('PlayerUpdate','{"sequence": 3, "playerid": "Paula"}')
    except Exception as e:
        # Above message is missing fields for x/y.  Could this be caught?
        print("Very good creator!")

# Uncomment when ready
test_recreator()

# -----------------------------------------------------------------------------
# Exercise 2 - The Receiver
#
# To receive a message on a network connection, you've got to write
# code that receives fragments of bytes and reassembles them back into
# message objects.
#
# A common object used for network communication is a "socket".  A socket
# has a method sock.recv(maxsize) that receives bytes (up to a requested
# maximum size).  It returns an empty byte-string when a connection is
# closed.
#
# Your task is to write a generator function that reads raw bytes off
# of a socket and produces fully formed Message instances using the
# recreate_message() function you just wrote. Here's a skeleton:

def receive_messages(sock):
    # problem.
    # we will get some stream of bytes off the network. but it's going to
    # show up as fragments of unpredictable size.  Thus, we have to collect all of
    # these fragments and reassemble them into complete messages shomehow
    #
    buffer = bytearray()
    while True:
        # A message must have at least 2 complete lines of text in it
        #  <message type>\r\n
        #  <message size>\r\n
        # if we don't have this, we have to read more data
        while buffer.count(b'\r\n') < 2:
            chunk = sock.recv(100000)    # Receive some data (actual size unknown)
            if chunk == b'':
                return     #the other end of the connection got closed. No more data will follow
            buffer.extend(chunk)

        b_msgtype, b_msgsz, buffer = buffer.split(b'\r\n', 2)
        msgsz = int(b_msgsz)
        while len(buffer) < msgsz:  # incomplete payload. keep reading data
            chunk = sock.recv(100000)
            if chunk == b'':
                return
            buffer.extend(chunk)
        b_playload = buffer[:msgsz]
        del buffer[msgsz:]    # consumed the payload part. maybe extra stuff in buffer (next message)

        # Reconstitute a message from the data (you implement)
        yield recreate_message(b_msgtype.decode('utf-8'), b_playload.decode('utf-8'))


# This test requires the use of the 'testmsg.py' script in this same directory.
# It must be running in a separate Python process (open a separate terminal
# window and run it there).
def test_receiver():
    print("Testing receiver")
    import socket
    sock = socket.create_connection(('localhost', 10000))
    messages = []
    for msg in receive_messages(sock):
        messages.append(msg)
    msg1 = messages[0]
    assert isinstance(msg1, ChatMessage) and \
           msg1.sequence == 1 and \
           msg1.playerid == 'Dave' and \
           msg1.text == 'Hello World'

    msg2 = messages[1]
    assert isinstance(msg2, PlayerUpdate) and \
        msg2.sequence == 2 and \
        msg2.playerid == 'Paula' and \
        msg2.x == 23 and \
        msg2.y == 41

    sock.close()
    print('Good receiver!')

# Uncomment when ready
test_receiver()

# -----------------------------------------------------------------------------
# Exercise 3 - The Async
#
# After spending the entirety of self-imposed quarantine reading "Hacker News",
# The project manager has decided that it's critically important for
# messages to be received using "async" code instead of a normal
# Python function.  Thus, he has requested a new implementation of
# receive_messages() that makes use of Python's asyncio module instead.
#
# If you've never used asyncio before, this is not going to be a tutorial.
# However, asyncio provides a similar sock.recv() operation. It just
# looks a bit different.  Here's a skeleton of the code you need to write:

import asyncio

async def areceive_messages(sock):
    loop = asyncio.get_event_loop()

    buffer = bytearray()
    while True:
        # A message must have at least 2 complete lines of text in it
        #  <message type>\r\n
        #  <message size>\r\n
        # if we don't have this, we have to read more data
        while buffer.count(b'\r\n') < 2:
            chunk = await loop.sock_recv(sock, 100000)
            if not chunk:
                break
            buffer.extend(chunk)

        b_msgtype, b_msgsz, buffer = buffer.split(b'\r\n', 2)
        msgsz = int(b_msgsz)
        while len(buffer) < msgsz:  # incomplete payload. keep reading data
            chunk = await loop.sock.recv(100000)
            if chunk == b'':
                return
            buffer.extend(chunk)
        b_playload = buffer[:msgsz]
        del buffer[msgsz:]    # consumed the payload part. maybe extra stuff in buffer (next message)

        # Reconstitute a message from the data (you implement)
        yield recreate_message(b_msgtype.decode('utf-8'), b_playload.decode('utf-8'))


# This test requires the use of the 'testmsg.py' script in this same directory.
# It must be running in a separate Python process (open a separate terminal
# window and run it there).
async def test_areceiver():
    print("Testing areceiver")
    import socket
    sock = socket.create_connection(('localhost', 19000))
    sock.setblocking(False)
    messages = []
    async for msg in areceive_messages(sock):
        messages.append(msg)

    msg1 = messages[0]
    assert isinstance(msg1, ChatMessage) and \
           msg1.sequence == 1 and \
           msg1.playerid == 'Dave' and \
           msg1.text == 'Hello World'

    msg2 = messages[1]
    assert isinstance(msg2, PlayerUpdate) and \
        msg2.sequence == 2 and \
        msg2.playerid == 'Paula' and \
        msg2.x == 23 and \
        msg2.y == 41

    sock.close()
    print('Good async receiver!')

# Uncomment to run the above test
#asyncio.run(test_areceiver())

# -----------------------------------------------------------------------------
# Exercise 4 - **DRY (Don't Repeat Yourself)** (Don't Repeat Yourself)
#
# For better or for worse, I/O handling in Python is split between two
# worlds.  There's the world of normal "synchronous" functions and threads
# (exercise 2) and the world of "asynchronous" functions (exercise 3).
# Unfortunately, these two execution models are basically incompatible
# with each other.  For example, if you tried to use the
# `receive_messages()` function from Exercise 2 inside of async code,
# it would block the internal event loop and prevent anything else
# from running.  Likewise, the `areceive_messages()` function from
# Exercise 3 can't even be called from normal Python functions because
# it requires the use of an "async" for-loop or an "await".
#
# A well-known rant about this problem can be found here:
#
#   https://journal.stuffwithstuff.com/2015/02/01/what-color-is-your-function/
#
# However, this split between "sync" and "async" also presents a real
# programming challenge.  In many applications, there is critical
# "business logic" that is at the heart of what you are doing (i.e.,
# solving the actual problem).  You may not want to anchor it to a
# specific implementation of I/O.
#
# An example of this is the code that implements the message decoding
# protocol in earlier exercises.  There's a pretty good chance that your
# implementations of `receive_messages()` and `areceive_messages()`
# are almost identical.  Yet, does most of that code need to be
# duplicated?   That is the challenge.
#
# Your task: Can you refactor the receive_messages() and
# areceive_messages() functions so that the protocol-related code is
# only implemented ONCE.  Here, "protocol" refers to the code that
# recognizes and decodes the parts needed to reconstruct Message
# objects (i.e., the message type, size, JSON payload, etc.).
# Can that code be isolated in some manner that makes it usable from
# any I/O implementation?
#
# Note: Implementing I/O-independent protocols is increasingly common
# in Python.  See https://sans-io.readthedocs.io.

class MessageDecoder:
    # idea
    # an object that has received data fed to it.
    # it then produces messages  (if any)
    #
    def __init__(self):
        self.buffer = bytearray()

    def feed(self, data):
        self.buffer.extend(data)  # where data comes from? no idea

    def messages(self):
        #produce all messages that can be found in the data so far
        #
        # A message must have at least 2 complete lines of text in it
        #  <message type>\r\n
        #  <message size>\r\n
        # if we don't have this, we have to read more data until we at least have that
        while self.buffer.count(b'\r\n') >= 2:
            b_msgtype, b_msgsz, remaining = self.buffer.split(b'\r\n', 2)
            msgsz = int(b_msgsz)
            if len(remaining) < msgsz:  # incomplete payload. keep reading data
                return
            b_playload = remaining[:msgsz]
            self.buffer = remaining[msgsz:]
            
            # Reconstitute a message from the data (you implement)
            yield recreate_message(b_msgtype.decode('utf-8'), b_playload.decode('utf-8'))

def receive_messages(sock):
    print("NEW receive_messages")
    decoder = MessageDecoder()
    while True:
        # produce message
        for msg in decoder.messages():
            yield msg
        chunk = sock.recv(100000)
        if chunk == b'':
            break
        decoder.feed(chunk)  # feed the data

async def areceive_messages(sock):
    loop = asyncio.get_event_loop()
    print("NEW receive_messages")
    decoder = MessageDecoder()
    while True:
        for msg in decoder.messages():
            yield msg
        chunk = sock.recv(100000)
        if chunk == b'':
            break
        decoder.feed(chunk)

test_receiver()
asyncio.run(test_areceiver())


def _receive_messages(sock):

    buffer = bytearray()
    while True:
        # A message must have at least 2 complete lines of text in it
        #  <message type>\r\n
        #  <message size>\r\n
        # if we don't have this, we have to read more data
        while buffer.count(b'\r\n') < 2:
            chunk = ... #
            if not chunk:
                break
            buffer.extend(chunk)

        b_msgtype, b_msgsz, buffer = buffer.split(b'\r\n', 2)
        msgsz = int(b_msgsz)
        while len(buffer) < msgsz:  # incomplete payload. keep reading data
            chunk = ... #
            if chunk == b'':
                return
            buffer.extend(chunk)
        b_playload = buffer[:msgsz]
        del buffer[msgsz:]    # consumed the payload part. maybe extra stuff in buffer (next message)

        # Reconstitute a message from the data (you implement)
        yield recreate_message(b_msgtype.decode('utf-8'), b_playload.decode('utf-8'))
