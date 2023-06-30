from flask_app import app
from flask_app.models.friend import Friend
from flask_app.models.recc import Recc
from flask_app.models.user import User
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def login_page():
    return render_template("create.html")

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'GET':
        return render_template("create.html")
    else:
        if not User.validate_create(request.form):
            return redirect('/')
        pw_hash = bcrypt.generate_password_hash(request.form['pword'])
        data = {
            "fname": request.form['fname'],
            "lname": request.form['lname'],
            "uname": request.form['uname'],
            "email": request.form['email'],
            "pword": pw_hash
        }
        User.create_user(data)
        flash("You made an Account!", "success")
        return redirect('/')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        data = {"email": request.form["email"]}
        user = User.select_by_email(data)
        if not user:
            flash("Invalid Email/Password", "login")
            return redirect('/login')
        if not bcrypt.check_password_hash(user.password, request.form["pword"]):
            flash("Invalid Email/Password", "login")
            return redirect('/login')
        session["user_id"] = user.id
        return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if "user_id" not in session:
        return redirect('/')
    data = {"id": session["user_id"]}

    print("USERS Data Dictionarii ####", data)
    frienda = Friend.select_UserFriends(data)
    logged_user = User.select_loggedUser(data)
    friends = Friend.selectPending_withSender(data)
    friendr = Friend.selectPending_withReciever(data)
    my_reccs = Recc.select_allReccs_userid(data)
    return render_template("dashboard.html", user=logged_user, friends=friends, friendr=friendr, frienda=frienda, my_reccs=my_reccs)
