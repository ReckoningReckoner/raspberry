from wtforms import TextField, IntegerField, BooleanField
from wtforms import Form, validators


class NewRemote(Form):
    def to_json(self, form):
        raise NotImplementedError("abstract method not overriden")


class NewLED(NewRemote):
    name = TextField("Name(*)", [validators.Required(message="Name must not" +
                     " be left blank")])

    pin = IntegerField("GPIO pin(*)", [validators.NumberRange(4, 26,
                       message="GPIO pin must be a valid integer between" +
                       " 4-26"), validators.Required(message="GPIO pin must" +
                                                             " not be" +
                                                             " left blank")])

    keep_on = BooleanField("Turn on after submission?")
    remote_type = "LED"

    # Takes a wtform cass and returns a json type
    def to_dic(self, form):
        return {
                   "type": form.remote_type,
                   "pin": form.pin.data,
                   "name": form.name.data,
                   "keep_on": form.keep_on.data
               }
