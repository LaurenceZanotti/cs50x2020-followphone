from flask import flash, session, redirect
from functools import wraps

def login_required(f):
    """
    Route decorators to check if user is logged in

    Based on Problem Set 8 Finance implementation
    and Flask's view decorators (also mentioned in
    pset8 code comments:
    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/)

    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            flash("You must login first!", "warning") # Give user feedback
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function



