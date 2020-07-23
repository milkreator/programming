

# state machine pattern
class Connection:
    def __init__(self):
        self.mode = ClosedMode

    def open(self):
        self.mode = OpenMode

    def close(self):
        self.mode = ClosedMode    # Mode is not an "instance"

    def receive(self):
        self.mode.receive(self)   # The "Connection" instance is passed as the self to the mode methods.

    def send(self):
        self.mode.send(self)

class ClosedMode:
    def receive(self):
        raise RuntimeError("Closed")

    def send(self):
        raise RuntimeError("Closed")

class OpenMode:
    def receive(self):
        print('Receiving')

    def send(self):
        print('Sending')