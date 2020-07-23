

class MyObject():
    def __new__(cls):
        #called to create the instance
        print("new")
        return super().__new__(cls)
    def __init__(self):
        # init, after the creation
        print("init")
        self.x = 2
        self.y = 3

    def __del__(self):
        # ref count = 0
        print("del")

p = MyObject()
p.__dict__

print