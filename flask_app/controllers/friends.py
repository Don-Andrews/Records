from flask_app import app
from flask_app.models.friend import Friend
from flask import render_template, redirect, request, session, flash

@app.route('/sendfriend', methods=['POST'])
def send_friend():
    data = {
        "friend_id": request.form["recevier_id"],
        "user_id": session["user_id"],
    }
    Friend.create_friend(data)
    return redirect('/dashboard')

@app.route('/accept', methods=['POST'])
def accept_friend():
    data = {
        "sendid": request.form["sender_id"],
        "recid": session["user_id"]
    }
    Friend.accept_friend(data)
    return redirect('/dashboard')

@app.route('/deletefriends', methods=['POST'])
def delete_FS():
    data = {
        "sendid": session["user_id"],
        "recid": request.form["recevier_id"]
    }
    Friend.delete_as_sender(data)
    return redirect(f'/{request.form["recevier_id"]}/reccPage')

@app.route('/deletefriendr', methods=['POST'])
def delete_FR():
    data = {
        "sendid": session["user_id"],
        "recid": request.form["sender_id"]
    }
    Friend.delete_as_reciever(data)
    return redirect(f'/{request.form["sender_id"]}/reccPage')

@app.route('/deny', methods=['POST'])
def deny_friends():
    data = {
        "sendid": session["user_id"],
        "recid": request.form["sender_id"]
    }
    Friend.delete_as_reciever(data)
    return redirect(f'/{request.form["sender_id"]}/reccPage')