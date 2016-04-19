# This module is the web server, and communictates to the remote.py module


from flask import Flask, request, flash, redirect, url_for, render_template
from threading import Thread
from backend.remote import Remote
from backend.remote_object import RemoteSimpleOutput
import traceback

app = Flask(__name__)
app.secret_key = "I love Gloria"


def get_relevant_form(remote_type):
    if remote_type == "SimpleOutput":
        return RemoteSimpleOutput.Form(request.form)
    else:
        return None


@app.route("/edit")
@app.route("/new")
def new_RemoteOption():
    return redirect(url_for("index"))


@app.route("/new/<remote_type>", methods=['GET', 'POST'])
def new_Remote(remote_type):
    form = get_relevant_form(remote_type)

    if form is None:  # this means that the form doesn't exist in the db
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
            return render_template('register.html', form=form,
                                   remote_type=remote_type)
        except Exception as e:
            flash(traceback.format_exc())
            flash(e)
            return render_template('register.html', form=form,
                                   remote_type=remote_type)

    elif request.method == "GET":
        return render_template('register.html', form=form,
                               remote_type=remote_type)


@app.route("/edit/<pin>", methods=["GET", "POST"])
def edit(pin):

    data = r.get_remote_data(pin)
    if data is None:
        return redirect(url_for("index"))

    form = get_relevant_form(data["type"])

    if request.method == "POST":
        if "delete" in request.form:
            r.delete(pin)
            return redirect(url_for("index"))
        elif "edit" in request.form:
            try:

                print("FORM ABOUT TO SEND IS", form.to_dic(form))
                if not form.validate():  # form not filled out properly
                    for error in form.errors.values():
                        flash("".join(error))
                    raise ValueError("Cannot Validate Form")

                r.update_remote(pin, form.to_dic(form))
                print("new db", r.to_dict())
                return redirect(url_for("index"))  # success!

            except ValueError as e:  # display error
                flash(e)
                return render_template("edit.html",
                                       remote_type=data["type"],
                                       form=form,
                                       remote=data)
            except Exception as e:
                flash(traceback.format_exc())
                flash(e)
                return render_template("edit.html",
                                       remote_type=data["type"],
                                       form=form,
                                       remote=data)

    return render_template("edit.html",
                           remote_type=data["type"],
                           form=form,
                           remote=data)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        if "toggle" in request.form:
            pin = request.form["toggle"]
            r.toggle(int(pin))

    return render_template('home.html',
                           remotes=r.to_dict(),
                           valid_types=r.valid_types)


if __name__ == "__main__":
    r = Remote()
    r_thread = Thread(target=r.run)
    r_thread.daemon = True
    r_thread.start()
    app.run(debug=True, host='0.0.0.0', use_reloader=True)
