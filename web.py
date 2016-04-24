# This module is the web server, and communictates to the remote.py module

from flask import Flask, request
from flask import flash, redirect
from flask import url_for, render_template
from flask import session

from threading import Thread
from backend.remote import Remote
import traceback
import bcrypt
import json

app = Flask(__name__)
{'bigbrother': {'hash': b'$2b$12$s5Jq12SE71MTTVH8TRn53OkdSCOOI8zjkk1DufZogUKIKrRZfxaDO'} }
users = 


# ===== For logging in an out of a page ========

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        if username in users and \
            bcrypt.hashpw(bytes(request.form['password']),
                          users[username]['hash']) == \
                users[username]['hash']:

            session['logged_in'] = request.form['username']
            return redirect(url_for('index'))

        flash("Incorrect username or password")

    return render_template("login.html")


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for("login"))


# ===== For displaying the front page of the website =====

@app.route("/", methods=['GET', 'POST'])
def index():
    if not session.get('logged_in'):
        return redirect(url_for("login"))

    if request.method == "POST":
        if "toggle" in request.form:
            pin = request.form["toggle"]
            r.toggle(int(pin), "keep_on")
        elif "photo_toggle" in request.form:
            pin = request.form["photo_toggle"]
            r.toggle(int(pin), "photo_toggle")

    return render_template('home.html',
                           remotes=r.to_dict(),
                           valid_types=r.valid_types)


# ======= For adding remotes to the database and editing them ======


@app.route("/new/<remote_type>", methods=['GET', 'POST'])
def new_Remote(remote_type):
    if not session.get('logged_in'):
        return redirect(url_for("login"))

    Remote_Class = r.get_relevant_type(remote_type)
    form = Remote_Class.Form(request.form)

    if form is None:  # this means that the form doesn't exist in the db
        return redirect(url_for("new_RemoteOption"))

    if request.method == "POST":
        try:
            if not form.validate():  # form not filled out properly
                for error in form.errors.values():
                    flash("".join(error))
                raise ValueError

            r.add(Remote_Class.to_dic(form))
            return redirect(url_for("index"))  # success!

        except ValueError as e:  # display error
            flash(e)
            return render_template('register.html', form=form,
                                   remote_type=remote_type,
                                   remote=Remote_Class.to_dic(form))
        except Exception as e:  # Usually an internal error
            flash(traceback.format_exc())
            flash(e)
            return render_template('register.html', form=form,
                                   remote_type=remote_type,
                                   remote=Remote_Class.to_dic(form))

    return render_template('register.html', form=form,
                           remote_type=remote_type)


@app.route("/edit/<pin>", methods=["GET", "POST"])
def edit(pin):
    if not session.get('logged_in'):
        return redirect(url_for("login"))

    data = r.get_remote_data(pin)
    if data is None:
        return redirect(url_for("index"))

    Remote_Class = r.get_relevant_type(data["type"])
    form = Remote_Class.Form(request.form)

    if request.method == "POST":
        if "delete" in request.form:
            r.delete(pin)
            return redirect(url_for("index"))
        elif "edit" in request.form:
            try:
                if not form.validate():  # form not filled out properly
                    for error in form.errors.values():
                        flash("".join(error))
                    raise ValueError("Cannot Validate Form")

                r.update_remote(pin, Remote_Class.to_dic(form))
                print("new db", r.to_dict())
                return redirect(url_for("index"))  # success!

            except ValueError as e:  # display error
                flash(e)
                return render_template("edit.html",
                                       remote_type=data["type"],
                                       form=form,
                                       remote=data)
            except NotImplementedError as e:
                flash("Internal Error. Method or class was not found")
                flash(e)
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


if __name__ == "__main__":
    r = Remote()
    r_thread = Thread(target=r.run)
    r_thread.daemon = True
    r_thread.start()

    app.config["SECRET_KEY"] = "I love gloria <3"
    app.run(debug=True, host='0.0.0.0', use_reloader=False)
