# This module is the web server, and communictates to the remote.py module


from flask import Flask, request, flash, redirect, url_for, render_template
from threading import Thread
from backend.remote import Remote
from backend.remote_object import RemoteSimpleOutput
import traceback

app = Flask(__name__)
app.secret_key = "I love Gloria"


@app.route("/new")
def new_RemoteOption():
    return redirect(url_for("index"))


@app.route("/new/<remote_type>", methods=['GET', 'POST'])
def new_Remote(remote_type):
    print(remote_type)
    if remote_type == "SimpleOutput":
        form = RemoteSimpleOutput.Form(request.form)
    else:
        return redirect(url_for("new_RemoteOption"))

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
        return render_template('register.html', form=form,
                               remote_type=remote_type)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        if "toggle" in request.form:
            pin = request.form["toggle"]
            r.toggle(int(pin))
        elif "delete" in request.form:
            pin = request.form["delete"]
            r.delete(int(pin))

        print("YOLO", r.valid_types)

    return render_template('home.html',
                           remotes=r.to_dict(),
                           valid_types=r.valid_types)


if __name__ == "__main__":
    r = Remote()
    r_thread = Thread(target=r.run)
    r_thread.daemon = True
    r_thread.start()
    app.run(debug=True, host='0.0.0.0', use_reloader=True)
