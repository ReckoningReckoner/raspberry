from tinydb import TinyDB, Query
from time import sleep, time
from remote_object import RemoteLED


# Class for holding all the remotes

class Remote():
    def __init__(self):
        self.db = TinyDB("database.json")
        self.query = Query()
        print("Loaded Database")

        self.remotes = {}
        for remote in self.to_dict():
            self.add_locally(remote)

        print("created remotes")

    # runs in parallel with the flask server, for physically
    # displaying the lights (or lack of)
    def run(self):
        print("Running Remotes")

        while True:
            try:
                sleep(1) # Prevents the system from going too fast
                to_debug = self.show_debug_output()
                self.run_the_remotes(to_debug)

            except RuntimeError as e:
                print(e)
                print("Continuing anyway")
                continue

    # Debug output
    def show_debug_output(self):
        current_time = int(time())
        debug = current_time % 5 == 0
        if debug:
            print("Time is: ", current_time, "\n")
            print("size of db:", len(self.db))
            print("size of remotes:", len(self.remotes))

        return debug

    # Runs all the remotes
    def run_the_remotes(self, debug=True):
        for remote in self.to_dict(): # use the database to find things
            pin = remote['pin']
            if pin in self.remotes:
                self.remotes[pin].input(remote)
                self.remotes[pin].output(self.db, self.query)

                if debug:
                    print("db", remote)

    # checks if it's a duplicate
    def check_for_duplicate_pin(self, d={}, pin=None):
        if pin == None:
            result = self.db.get(self.query["pin"] == d["pin"])
        else:
            result = self.db.get(self.query["pin"] == pin)

        if result is not None:  # GPIO duplicate pin error
            raise ValueError("GPIO Pin in use either" +
                             " change this pin or delete" +
                             " the remote currently using " +
                             " this pin")

    # adds to database
    def new_RemoteLED(self, remote):
        try:
            import copy
            r = RemoteLED(copy.deepcopy(remote))
            self.remotes[remote['pin']] = r
        except Exception as e:
            raise e

    # adds to remote dictionary only. Should onyl be used during init
    def add_locally(self, remote):
        if remote["type"] == "LED":
            self.new_RemoteLED(remote)
        else:
            raise TypeError("Invalid remote type")

    # adds to the dictionary and database
    def add(self, remote):
        try:
            self.check_for_duplicate_pin(d=remote)
            self.add_locally(remote)
            self.db.insert(remote)
            print("# of remotes is:", len(self.remotes))
        except Exception as e:
            raise e

    def to_dict(self):
        return self.db.all()

    #toggles a certain key
    def toggle(self, pin, key="keep_on"):
        if type(pin) is not int:
            pin = int(pin)

        result = self.db.get(self.query["pin"] == pin)

        if result[key]:
            new_bool = False
        else:
            new_bool = True

        self.db.update({key: new_bool}, self.query["pin"] == pin)

    def delete(self, pin):
        if type(pin) is not int:
            pin = int(pin)

        if pin not in self.remotes:
            return

        self.remotes.pop(pin)
        self.db.remove(self.query["pin"] == pin)

if __name__ == "__main__":
    print("nothing to do!")
