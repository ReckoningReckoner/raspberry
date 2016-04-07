from flask import Flask, request, flash, redirect, url_for, render_template
from threading import Thread
from remote import Remote
from textFill import NewLED
import traceback

app = Flask(__name__)
app.secret_key = "I love Gloria"


@app.route("/new", methods=['GET', 'POST'])
def new_Remote():
    form = NewLED(request.form)

    if request.method == "POST":

        try:
            if not form.validate():  # form not filled out properly
                for error in form.errors.values():
                    flash("".join(error))
                raise ValueError("Unable to validate form")

            r.add(form.to_dic(form))
            return redirect(url_for("index"))  # success!

        except ValueError as e:  # display error
            flash(e)
            return render_template('register.html', form=form)
        except Exception as e:
            flash(traceback.format_exc())
            flash(e)
            return render_template('register.html', form=form)

    elif request.method == "GET":
        return render_template('register.html', form=form)
    else:
        raise RuntimeError("invalid request method")


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template('home.html', remotes=r.to_dict())
    elif request.method == "POST":
        pin = request.form["toggle"]
        r.toggle(int(pin))
        return render_template('home.html', remotes=r.to_dict())
    else:
        raise RuntimeError("invalid request method")


def start_web_server():
    app.run(debug=True, host='0.0.0.0')

if __name__ == "__main__":
    r = Remote()
    r_thread = Thread(target=r.run)
    r_thread.daemon = True
    r_thread.start()
    app.run(debug=True, host='0.0.0.0')
