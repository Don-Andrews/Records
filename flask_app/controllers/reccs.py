from flask_app import app
from flask_app.models.user import User
from flask_app.models.friend import Friend
from flask_app.models.recc import Recc
from flask import render_template, redirect, request, session, flash


@app.route('/search_user', methods=['POST'])
def search_user():
    users = User.search_username(request.form["user_name"])
    users_dict = []
    for user in users:
        users_dict.append(user.to_dict())
    return users_dict

@app.route('/<int:user_id>/reccPage')
def user_page(user_id):
    if "user_id" not in session:
        return redirect('/')
    if user_id == session["user_id"]:
        return redirect('/dashboard')
    data = {"id": session["user_id"]}
    data2 = {"id": user_id}
    fdata = {"id":session["user_id"], "fu_id": user_id}
    friendsr = Friend.select_if_friends(fdata)
    friendrr = Friend.select_if_friendr(fdata)
    logged_user = User.select_loggedUser(data)
    other_user = User.select_by_id(user_id)
    user_reccs = Recc.select_allReccs_userid(data2)
    return render_template("user_page.html", logged_user=logged_user, other_user=other_user, fs=friendsr, fr=friendrr, user_reccs=user_reccs)

@app.route('/allreccs')
def friendsRecc_page():
    if "user_id" not in session:
        return redirect('/')
    data = {"id": session["user_id"]}
    logged_user = User.select_loggedUser(data)
    users = User.select_all()
    reccs = Recc.select_allReccs_Users()
    return render_template("allreccs.html", user=logged_user, users=users, reccs=reccs)

@app.route('/makerecc')
def makeRecc_page():
    if "user_id" not in session:
        return redirect('/')
    data = {"id": session["user_id"]}
    logged_user = User.select_loggedUser(data)
    return render_template("makerecc.html", user=logged_user)

@app.route('/make/recc', methods=['POST'])
def make_recc():
    if not Recc.validate_recc(request.form):
        return redirect('/makerecc')
    data = {
        "title": request.form['title'],
        "aname": request.form['artist'],
        "aors": request.form['aors'],
        "pop": request.form['pop'],
        "hon": request.form['heard_on'],
        "uid": request.form['u_id']
    }
    Recc.create_recc(data)
    return redirect('/dashboard')

@app.route('/deleterecc', methods=['POST'])
def delete_recc():
    data = {"id": request.form['id']}
    Recc.delete_recc(data)
    return redirect('/dashboard')

@app.route('/edit/recc/<int:recc_id>')
def edit_page(recc_id):
    if "user_id" not in session:
        return redirect('/')
    data = {"id": session["user_id"]}
    logged_user = User.select_loggedUser(data)
    recc = Recc.select_one(recc_id)
    return render_template("editrecc.html", user=logged_user, recc=recc)

@app.route('/edit/recc', methods=['POST'])
def edit_recc():
    if not Recc.validate_recc(request.form):
        return redirect(f"/edit/recc/{request.form['u_id']}")
    data = {
        "title": request.form['title'],
        "aname": request.form['artist'],
        "aors": request.form['aors'],
        "pop": request.form['pop'],
        "hon": request.form['heard_on'],
        "u_id": request.form['u_id']
    }
    Recc.update_recc(data)
    return redirect('/dashboard')

@app.route('/settings')
def settings_page():
    if "user_id" not in session:
        return redirect('/')
    data = {"id": session["user_id"]}
    logged_user = User.select_loggedUser(data)
    return render_template("settings.html", user=logged_user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')