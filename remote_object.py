# Keep true if not coding from RPI
DEBUG = False 

from tinydb import TinyDB, Query

if not DEBUG:
    from gpiozero import LED

class RemoteAbstract():
    def __init__(self, dic):
        self.__dict__ = dic
        getattr(self, "pin")

    def input(self, data):
        pass
    
    def output(self, database, query):
        pass


class RemoteLED(RemoteAbstract):
    def __init__(self, dic):
        super().__init__(dic)
        if DEBUG:
            pass
        else:
            try:
                self.led = LED(dic["pin"])
            except Exception as e:
                raise e

    def input(self, data):
        if DEBUG:
            pass
        else:
            if data["keep_on"]:
                self.led.on()
            else:
                self.led.off()

