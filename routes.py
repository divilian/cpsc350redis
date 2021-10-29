
from flask import request, url_for, session, render_template, redirect
from hobbies import hobby_mgr
import redis

@hobby_mgr.route("/")
def login_or_register():
    r = redis.StrictRedis(password="davies4ever", charset='utf-8',
        decode_responses=True)
    if ('user' in session and
        session['password'] == r.get("user:"+session['user'])):
        return redirect(url_for("show_hobby_list"))
    else:
        return render_template("login_or_register.html")

@hobby_mgr.route("/show_hobby_list")
def show_hobby_list():
    if 'user' not in session:
        return redirect(url_for("login_or_register"))
    r = redis.StrictRedis(password="davies4ever", charset='utf-8',
        decode_responses=True)
    hobbies = r.smembers("hobbies:"+session['user'])
    return render_template("show_hobby_list.html", hobbies=hobbies,
        user=session['user'])

@hobby_mgr.route("/register", methods=['POST'])
def register():
    username = request.form['username'] 
    password1 = request.form['password'] 
    password2 = request.form['password2'] 
    if password1 != password2:
        return render_template("login_or_register.html",
            msg="passwords don't match. :(")
    r = redis.StrictRedis(password="davies4ever", charset='utf-8',
        decode_responses=True)
    if r.exists("user:"+request.form["username"]):
        return render_template("login_or_register.html",
            msg=f"Sorry, username {username} already taken!")
    r.set("user:"+username, password1)
    session["user"] = username
    session["password"] = password1
    return redirect(url_for("show_hobby_list"))

@hobby_mgr.route("/login")
def login():
    return "TODO!"

@hobby_mgr.route("/add_or_remove")
def add_or_remove():
    r = redis.StrictRedis(password="davies4ever", charset='utf-8',
        decode_responses=True)
    hobby = request.args['hobby']
    username = session['user']
    if (r.exists("hobbies:"+username) and
        r.sismember("hobbies:"+username,hobby)):
        r.srem("hobbies:"+username, hobby)
    else:
        r.sadd("hobbies:"+username, hobby)
    return redirect(url_for('show_hobby_list'))
    
