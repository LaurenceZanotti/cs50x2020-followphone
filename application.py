import os

from flask import Flask, flash, render_template, redirect, request, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from utilities import login_required

# Import flask functions
app = Flask(__name__)

# Database configuration
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/followphone.db'
db = SQLAlchemy(app)

app.secret_key = os.getenv('SECRET_KEY')

"""
Load tables

https://www.reddit.com/r/flask/comments/31etxm/how_can_i_use_sqlalchemy_reflection_or_metadata/
https://docs.sqlalchemy.org/en/13/orm/extensions/automap.html?highlight=automap#module-sqlalchemy.ext.automap
Table reflection doesn't really map the DB. So Automap is needed to be able to insert and delete, instead of just selecting

# users = db.Table('users', db.metadata, autoload=True, autoload_with=db.engine)
"""
# Reflect the existing database
Base = automap_base()
Base.prepare(db.engine, reflect=True)

# Load tables
Users = Base.classes.users
Contacts = Base.classes.contacts
Historys = Base.classes.historys
Talks = Base.classes.talks


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached (based on pset8 Finance flask config,
# to ensure changes are visible in the browser.
# https://cs50.harvard.edu/x/2020/tracks/web/finance/#applicationpy)
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    print(session)
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        # Register handler
        if "register-form" in request.form:
            # Get form values
            username = request.form.get("username")
            password = request.form.get("password")
            confirmation = request.form.get("confirmation")

            # Ensure form is valid
            if not username:
                flash("Must provide username", "danger")
                return redirect("/")

            if not password:
                flash("Must provide a password", "danger")
                return redirect("/")

            if not confirmation:
                flash("Must confirm your password", "danger")
                return redirect("/")

            if password != confirmation:
                flash("Passwords don't match", "warning")
                return redirect("/")

            # Queries db to check if username exists
            check = db.session.query(Users).filter_by(username=username).first()

            if check:
                flash("Username already exists", "danger")
                return redirect("/")

            # Adds user to db
            else:
                users = Users(username=username, hash=generate_password_hash(password))
                db.session.add(users)
                db.session.commit()


            flash("Account created successfully", "success")
            return redirect("/")

        # Login handler
        elif "login-form" in request.form:
            username = request.form.get("username")
            password = request.form.get("password")

            # Ensure forms are valid
            if not username or not password:
                flash("Must fill both username and password fields", "danger")
                redirect("/")

            # Check if user exists
            user = db.session.query(Users).filter_by(username=username).first()
            if not user:
                flash("This username does not exist.", "warning")
                return redirect("/")

            # Retrieve user data
            else:
                # Authenticate user by password
                if check_password_hash(user.hash, password):
                    # Clear sessions if there is any
                    session.clear()
                    # Save session
                    session['user_id'] = user.user_id
                    session['username'] = user.username
                else:
                    flash("Wrong password", "danger")
                    return redirect("/")

            flash("Logged in successfully!", "success")
            return redirect("/dashboard")

    # GET method
    else:
        return render_template("index.html")


@app.route("/signout")
@login_required
def signout():
    """ Log off the user """

    session.clear()

    flash("Logged off successfully", "success")

    return redirect("/")


@app.route("/dashboard")
@login_required
def dashboard():
    """ Main dashboard """

    # Queries for contact count
    contactCount = db.session.query(db.func.count(Contacts.contact_id)).filter_by(user_id = session["user_id"])

    for i in contactCount:
        # If there's no contacts, render template without parameters (first timer)
        if not i[0]:
            return render_template("maindash.html")
        else:
            contactCount = i[0]

    # Queries for urgent and not urgent historys,
    urgent = db.session.query(Historys.history_id, Historys.contact_id, Contacts.name, Contacts.lastname, Historys.subject, Historys.followup_datetime)\
        .join(Historys)\
        .filter_by(user_id = session["user_id"])\
        .filter(Historys.followup_datetime <= datetime.now().strftime("%Y-%m-%d %H:%M"))\
        .order_by(db.desc(Historys.followup_datetime))

    notUrgent = db.session.query(Historys.history_id, Historys.contact_id, Contacts.name, Contacts.lastname, Historys.subject, Historys.followup_datetime)\
        .join(Historys)\
        .filter_by(user_id = session["user_id"])\
        .filter(db.or_(Historys.followup_datetime >= datetime.now().strftime("%Y-%m-%d %H:%M"), Historys.followup_datetime == None))\
        .order_by(db.desc(Historys.followup_datetime))

    talksCount = db.session.query(db.func.count(Talks.talk_id)).join(Historys).filter_by(user_id = session["user_id"])

    table = []

    # Sort by param
    if not request.args.get("sortby") or request.args.get("sortby") == "urgent":
        # Sorts urgent historys first into the list by default (i.e. when there's no params)
        for item in urgent:
            table.append(item)

        for item in notUrgent:
            table.append(item)
    else:
        # Sort historys by not urgent first
        for item in notUrgent:
            table.append(item)

        for item in urgent:
            table.append(item)

    for i in talksCount:
        talksCount = i[0]

    return render_template("maindash.html", urgentHistorys=table, contactCount=contactCount, talksCount=talksCount)


@app.route("/contacts")
@login_required
def contacts():

    # If there's no results, render page with guides to add a contact
    check = db.session.query(Contacts).filter_by(user_id=session["user_id"]).first()
    if not check:
        return render_template("contacts.html")

    # Renders a table with the user's contacts
    query = db.session.query(Contacts).filter_by(user_id=session["user_id"])
    return render_template("contacts.html", tabledata=query)


@app.route("/contacts/add-contact", methods=["GET", "POST"])
@login_required
def addContact():

    if request.method == "POST":
        name = request.form.get("name")
        lastname = request.form.get("lastname")
        phone = request.form.get("phone")

        # Ensure all fields are filled
        if not name or not lastname or not phone:
            flash("You must fill all fields", "warning")
            return redirect("/contacts")

        # Adds the contact
        contact = Contacts(name=name, lastname=lastname, phone=phone, user_id=session["user_id"])
        db.session.add(contact)
        db.session.commit()

        flash(f"You added {name} {lastname} as your contact!", "success")


    return redirect("/contacts")


@app.route("/contacts/add-history", methods=["GET", "POST"])
@login_required
def addHistory():

    if request.method == "POST":
        subject = request.form.get("subject")
        followupdate = request.form.get("followupdate")
        followuptime = request.form.get("followuptime")
        contactId = request.form.get("contact-id")

        followup = None

        # Must have a contact to proceed
        if not contactId:
            flash("No contact was selected", "danger")
            return redirect("/contacts")

        # Ensure fields were filled
        if not subject:
            flash("You must fill at least the subject", "warning")
            return redirect("/contacts")

        # Check if follow up was provided and is formatted properly
        if not followupdate:
            pass
        else:
            # Ensure time is provided
            if not followuptime:
                flash("Must also provide the time of follow up", "warning")
                return redirect("/contacts")
            else:
                # Try to create a datetime object
                try:
                    followup = f"{followupdate} {followuptime}"
                    followup = datetime.strptime(followup, "%Y-%m-%d %H:%M")
                    followup = followup.strftime("%Y-%m-%d %H:%M")
                # If somehow the data is not properly formatted, advise the user
                except:
                    flash("Date and time must be formatted as the input demands", "danger")
                    return redirect("/contacts")


        # Add history to contact
        history = Historys(subject=subject, followup_datetime=followup, user_id=session["user_id"], contact_id=contactId)
        db.session.add(history)
        db.session.commit()
        flash("You created a history!", "success")


    return redirect("/historys")


@app.route("/historys", methods=["GET", "POST"])
@login_required
def historys():

    # If there's no historys
    check = db.session.query(Historys.history_id, Historys.contact_id).filter_by(user_id=session["user_id"]).first()
    if not check:
        return render_template("historys.html")

    # Queries historys and contacts to feed the historys table
    query = db.session.query(Historys.history_id, Historys.contact_id, Contacts.name, Contacts.lastname, Historys.subject, Historys.followup_datetime).join(Historys).filter_by(user_id=session["user_id"])

    # Save selected history to session (client is redirected to /history/viewtalks by clientside JS)
    if request.method == "POST":
        session["history"] = request.get_json()

    return render_template("historys.html", tabledata=query)


@app.route("/historys/viewtalks", methods=["GET", "POST"])
@login_required
def talks():

    # Check for session["history"] to see if a history was selected
    if session["history"]:
        # Queries history summary
        history = db.session.query(
            Historys.history_id,
            Historys.contact_id,
            Contacts.name,
            Contacts.lastname,
            Contacts.phone,
            Historys.subject,
            Historys.followup_datetime
        ).join(Historys).filter_by(history_id=session["history"]["historyid"]).filter_by(user_id = session["user_id"]).first()

        # Queries talks related to the selected history
        if not db.session.query(Talks).filter_by(history_id=session["history"]["historyid"]).first():
            talks = None # If there's no result
        else:
            talks = db.session.query(Talks).filter_by(history_id=session["history"]["historyid"]).order_by(Talks.datetime.desc())

    # If somehow the user access this page without selecting a history at /history
    else:
        # Render empty template with link to select a history
        return render_template("talks.html")

    # Create talk/note
    if request.method == "POST":
        conversation = request.form.get("conversation")
        service = request.form.get("service")
        followDate = request.form.get("followup_date")
        followTime = request.form.get("time")

        followup = None

        # Ensure form is filled
        if not conversation or not service:
            flash("Must fill at least conversation and service", "danger")
            return redirect("/historys/viewtalks")

        # If follow up date is provided
        if followDate:
            # Ensure time is also provided
            if not followTime:
                flash("You must provide the time", "danger")
                return redirect("/historys/viewtalks")
            else:
                # Try to create a datetime object and update history db
                try:
                    followup = f"{followDate} {followTime}"
                    followup = datetime.strptime(followup, "%Y-%m-%d %H:%M")
                    followup = followup.strftime("%Y-%m-%d %H:%M")
                # If somehow the data is not properly formatted, alert the user
                except:
                    flash("Date and time must be formatted as the input demands", "danger")
                    return redirect("/historys/viewtalks")


        # Add talk to history
        talk = Talks(conversation=conversation, service=service, datetime=datetime.now().strftime("%Y-%m-%d %H:%M"), history_id=session["history"]["historyid"])
        db.session.add(talk)
        db.session.commit()

        # Update history follow up
        stmt = db.update(Historys).where(Historys.history_id==session["history"]["historyid"]).values(followup_datetime=followup)
        db.engine.execute(stmt)

        flash("You created a new note!", "success")
        return redirect("/historys/viewtalks")

    # GET request
    else:
        return render_template("talks.html", history=history, talks=talks)


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    if request.method == "POST":
        if "change-password" in request.form:

            # Store args
            oldpass = request.form.get("oldpassword")
            newpass = request.form.get("newpassword")
            confpass = request.form.get("confirmation")

            # Ensure form is complete
            if not oldpass or not newpass or not confpass:
                flash("All fields must be filled", "danger")
                return redirect("/profile")

            # Queries db and checks if password matches or not
            hashed_pass = db.session.query(Users.hash).filter_by(user_id=session["user_id"]).first()

            if not check_password_hash(hashed_pass[0], oldpass):
                flash("Current password doesn't match", "danger")
                return redirect("/profile")

            # Check if the new password passes (is equal to) the confirmed one
            if newpass != confpass:
                flash("New password is not matching the confirmation", "warning")
                return redirect("/profile")

            # Generate hash and update user's password
            hashed_pass = generate_password_hash(newpass)

            stmt = db.update(Users).where(Users.user_id==session["user_id"]).values(hash=hashed_pass)
            db.engine.execute(stmt)

            flash("You've changed your password!", "success")
            return redirect("/profile")

    else:
        if "change-urgency" in request.args:
            flash("You've changed time of urgency", "info")

        return render_template("profile.html")

    return render_template("profile.html")
