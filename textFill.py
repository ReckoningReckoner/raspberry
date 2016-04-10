from wtforms import TextField, IntegerField, BooleanField
from wtforms import Form, validators

MIN_GPIO = 4
MAX_GPIO = 26


class NewRemote(Form):
    def to_json(self, form):
        raise NotImplementedError("abstract method not overriden")


class MinMaxIntegerField(IntegerField):
    def __init__(self, min=None, max=None, **kwargs):
        super().__init__(**kwargs)
        self.min = min
        self.max = max


class NewLED(NewRemote):
    name = TextField("Name", [validators.Required(message="Name must not" +
                     " be left blank")])

    blank_gpio_message = "GPIO pin must not be left blank"
    pin = MinMaxIntegerField(label="GPIO pin", min=MIN_GPIO, max=MAX_GPIO,
                             validators=[validators.Required(
                                         message=blank_gpio_message)])

    keep_on = BooleanField("Initial State")
    remote_type = "LED"

    # Takes a wtform cass and returns a json type
    def to_dic(self, form):
        return {
                   "type": form.remote_type,
                   "pin": form.pin.data,
                   "name": form.name.data,
                   "keep_on": form.keep_on.data
               }
