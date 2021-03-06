"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, 
                    flash, session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
  """ Homepage """

  return render_template("homepage.html")

@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route("/register", methods=["GET"])
def register_form():
    """Show registration form."""

    return render_template("register_form.html")

@app.route("/register", methods=["POST"])
def register_process():

    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    
    if not user:
        #create user in table
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        #adding email to the session(cookie one) makes the user log-in
        session["email"] = user.email
        return redirect ("/")
    else:
        return redirect("/log_in")

@app.route("/log_in", methods=["GET"])
def login_form():
    """Logs in uder."""

    return render_template("login_form.html")


@app.route("/log_in", methods=["POST"])
def login_process():
    """ Processes the log in email and password if the user is new."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    
    if user:
        if password == user.password:
            session["user_id"] = user.user_id
            flash("You were successfully logged in")
            return redirect("/")
        else:
            flash("Incorrect password")
            return redirect("/log_in")
    else:
        return redirect("/register")






if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000, host='0.0.0.0')
