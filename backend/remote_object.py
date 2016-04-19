# These are the remotes themselves. They are hardware devices that are
# controlled by the pi. They use wtforms to create attributes about them,
# such as which pin they are connected to the pi from


import wtforms
from wtforms import TextField, IntegerField, BooleanField
from wtforms import validators

DEBUG = True
if not DEBUG:  # if not editing from the raspberry pi
    from gpiozero import OutputDevice
else:
    print("DEBUG MODE IS ON, HARDWARE WILL NOT WORK")

MIN_GPIO = 4
MAX_GPIO = 26


# Has min max attributes so javascript can check if a pin is
# valid or not


class MinMaxIntegerField(IntegerField):
    def __init__(self, min=None, max=None, **kwargs):
        super().__init__(**kwargs)
        self.min = min
        self.max = max


# Abstract remote class. All Remotes should have a primary pin
# number and a name


class RemoteAbstract():
    def __init__(self, dic):
        self.pin = dic["pin"]
        self.name = dic["name"]

    def change_pin(self, new_pin):
        self.pin = new_pin

    # Gets information from database
    def input(self, data):
        self.pin = data["pin"]
        pass

    # Modifies database
    def output(self, database, query):
        pass

    def close(self):
        pass

    class Form(wtforms.Form):
        name = TextField("Name", [validators.Required(message="Name must not" +
                         " be left blank")])

        blank_gpio_message = "GPIO pin must not be left blank"
        wrong_pin_message = "GPIO pin must be between " +\
                            str(MIN_GPIO) + " - " + str(MAX_GPIO)

        pin = MinMaxIntegerField(label="GPIO pin", min=MIN_GPIO, max=MAX_GPIO,
                                 validators=[validators.Required(
                                                 message=blank_gpio_message),
                                             validators.NumberRange(
                                                 min=MIN_GPIO,
                                                 max=MAX_GPIO,
                                                 message=wrong_pin_message)])

        def to_dic(self, form):
            dic = {
                       "pin": form.pin.data,
                       "name": form.name.data
                   }
            return dic


# For devices that only have an on/off state


class RemoteSimpleOutput(RemoteAbstract):
    def __init__(self, dic):
        super().__init__(dic)

        if not DEBUG:
            try:
                self.device = OutputDevice(dic["pin"])
            except Exception as e:
                raise e

    def change_pin(self, pin):
        super().change_pin(pin)
        if not DEBUG:
            self.device = OutputDevice(pin)

    def input(self, data):
        if not DEBUG:
            if data["keep_on"]:
                self.device.on()
            else:
                self.device.off()

    def close(self):
        if not DEBUG:
            self.device.close()

    class Form(RemoteAbstract.Form):
        keep_on = BooleanField("Initial State")
        type = "SimpleOutput"

        def to_dic(self, form):
            dic = super().to_dic(form)
            dic["type"] = form.type
            dic["keep_on"] = form.keep_on.data
            return dic
