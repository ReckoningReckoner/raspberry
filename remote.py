from tinydb import TinyDB, Query


# Class for holding all the remotes

class Remote():
    def __init__(self):
        self.boolean = True
        self.valid_types = ["LED"]
        self.db = TinyDB("database.json")
        print("Loaded Database")
        self.remotes = {}

        for remote in self.to_dict():
            self.remotes[remote['pin']] = RemoteLED(remote)

    # runs in parallel with the flask server, for physically
    # displaying the lights (or lack of)
    def run(self):
        print("running remoteLED")
        while True:
            for k in self.remotes:
                self.remote[k].run()

    # checks if it's a duplicate
    def check_for_duplicate_pin(self, d):
        q = Query()
        result = self.db.get(q["pin"] == d["pin"])
        if result is not None:  # GPIO duplicate pin error
            raise ValueError("GPIO Pin in use either" +
                             " change this pin or delete" +
                             " the remote currently using " +
                             " this pin")

    # adds to database
    def new_RemoteLED(self, remote):
        self.db.insert(remote)
        self.remotes[remote['pin']] = RemoteLED(remote)

    # adds to the dictionary
    def add(self, d):
        try:
            self.check_for_duplicate_pin(d)
            if d["type"] == "LED":
                self.new_RemoteLED(d)
            else:
                raise TypeError("Invalid remote type")
        except Exception as e:
            raise e

    def to_dict(self):
        return self.db.all()

    def toggle(self, pin):
        if type(pin) is not int:
            pin = int(pin)

        q = Query()
        result = self.db.get(q["pin"] == pin)

        if result["keep_on"]:
            new_bool = False
        else:
            new_bool = True

        self.db.update({"keep_on": new_bool}, q["pin"] == pin)
        self.remotes[pin].set(self.db.get(q["pin"] == pin))


# Abstract remote class


class RemoteAbstract():
    def __init__(self, dic):
        self.__dict__ = dic
        getattr(self, "pin")

    def run(self):
        raise NotImplementedError

    def set(self, d):
        self.__dict__.update(d)


class RemoteLED(RemoteAbstract):
    def __init__(self, dic):
        super().__init__(dic)
        self.led = "LEDOBJECT"

        getattr(self, "keep_on")

    def run(self):
        if self.keep_on:
            pass
        else:
            pass

    def toggle(self):
        if self.keep_on:
            self.keep_on = False
        else:
            self.keep_on = True


if __name__ == "__main__":
    data = {'name': 'red', 'pin': 16, 'type': 'LED', 'keep_on': True}
    data2 = {'name': 'red', 'pin': 16, 'type': 'LED', 'keep_on': False}

    r = RemoteLED(data)
    print(r.__dict__)
    r.set(data2)
    print(r.__dict__)
    r.toggle()
    print(r.__dict__)
