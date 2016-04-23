# This class is the brdige between the web server, the remotes, and the
# database. It also gets input from the web server.
# The database is essentially a JSON file that has certain attributes.
# Those attributes can be used as an input for an ouput device, e.g.
# if a certain boolean is true, power the output device. Otherwise,
# turn it off.


from tinydb import TinyDB, Query
from time import time, sleep
import backend.remote_object


# Class for holding all the remotes
# TODO Fix duplicate errors
class Remote():
    def __init__(self):
        self.db = TinyDB("backend/database.json")
        self.query = Query()
        print("Loaded Database")

        self.valid_types = ["SimpleOutput",
                            "MotionSensor",
                            "Switch",
                            "AlarmSystem"]
        self.remotes = {}
        for remote in self.to_dict():
            self._add_locally(remote)

        print("created remotes")

    # runs in parallel with the flask server, for physically
    # displaying the lights
    def run(self):
        print("Running Remotes")

        while True:
            try:
                sleep(0.5)  # Prevents the system from going too fast
                to_debug = self._show_debug_output()
                self._run_the_remotes(to_debug)

            except RuntimeError as e:
                print(e)
                print("Continuing anyway")
                continue

    # Debug output
    def _show_debug_output(self):
        current_time = int(time())
        debug = current_time % 5 == 0
        if debug:
            print("Time is: ", current_time, "\n")
            print("size of db:", len(self.db))
            print("size of remotes:", len(self.remotes))

        return debug

    # Runs all the remotes
    def _run_the_remotes(self, debug=True):
        for remote in self.to_dict():  # use the database to find things
            pin = remote['pin']
            if pin in self.remotes:
                self.remotes[pin].input(remote)
                self.remotes[pin].output(self.db, self.query)

                if debug:
                    print("db", remote)

    # checks if it's a duplicate
    def _check_for_duplicate_pin(self, dic={}, pin=None):
        if pin is None:
            if "pins" in dic:  # a list of pin inside the dic
                try:
                    for pin_key in dic["pins"]:
                        self._check_for_duplicate_pin(pin=dic[pin_key])
                except ValueError as e:
                    raise e

            else:
                result = self.get_remote_data(dic["pin"])
        else:
            result = self.get_remote_data(pin)

        if result is not None:  # GPIO duplicate pin error
            raise ValueError("GPIO Pin in use either" +
                             " change this pin or delete" +
                             " the remote currently using " +
                             " this pin")

    # pass a name into method, will return relevant classs
    def get_relevant_type(self, remote_type):
        if remote_type in self.valid_types:
            return getattr(backend.remote_object, remote_type)
        else:
            return None

    # adds to remote dictionary only. Should onyl be used during init
    def _add_locally(self, remote):
        remote_class = self.get_relevant_type(remote["type"])
        if remote_class is not None:
            try:
                import copy
                r = remote_class(copy.deepcopy(remote))
                self.remotes[remote['pin']] = r
            except Exception as e:
                raise e

    # adds to the dictionary and database
    def add(self, remote):
        try:
            print(remote)
            self._check_for_duplicate_pin(dic=remote)
            self._add_locally(remote)
            self.db.insert(remote)

            print("# of remotes is:", len(self.remotes))
        except Exception as e:
            raise e

    # toggles a certain key
    def toggle(self, pin, key="keep_on"):
        if type(pin) is not int:
            pin = int(pin)

        result = self.get_remote_data(pin)

        if result[key]:
            new_bool = False
        else:
            new_bool = True

        self.update_remote(pin, {key: new_bool})
        # self.db.update({key: new_bool}, self.query["pin"] == pin)

    # deletes the remtoe from local memory
    def _delete_locally(self, pin):
        if type(pin) is not int:
            pin = int(pin)

        try:
            self.remotes[pin].close()  # Safely remove device
            self.remotes.pop(pin)
        except NotImplementedError as e:
            raise e

    # Delets from db and local copy
    def delete(self, pin):
        if type(pin) is not int:
            pin = int(pin)

        try:
            self.db.remove(self.query["pin"] == pin)
            self._delete_locally(pin)
        except NotImplementedError as e:
            raise e

    # change pin locally
    def _change_pin_locally(self, pin, dic):
        pin = int(pin)  # the old pin
        self.remotes[int(dic["pin"])] = self.remotes.pop(pin)

    # Updates database
    def update_remote(self, pin, dic):
        if type(pin) is not int:
            pin = int(pin)

        if "pin" in dic and int(dic["pin"]) != pin:  # switching pins
            try:
                self._check_for_duplicate_pin(dic=dic)
                self._change_pin_locally(pin, dic)
            except ValueError as e:
                raise e

        self.db.update(dic, self.query["pin"] == pin)

    # Returns value from db by pin
    def get_remote_data(self, pin):
        if type(pin) is not int:
            pin = int(pin)

        result = self.db.get(self.query["pin"] == pin)
        return result

    def to_dict(self):
        return self.db.all()

if __name__ == "__main__":
    print("nothing to do!")
