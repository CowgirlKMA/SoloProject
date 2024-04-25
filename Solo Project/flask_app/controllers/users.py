from flask_app import app, bcrypt
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
# from flask_app.models.user_model import User #User is the name of the class
#all of the class methods live in the the user_model.py file, we are importing the entire file 



@app.get("/")
def index():
#this route displays the login and registration forms
    return render_template("index.html")


@app.post("/users/register")
def register():
#this route processess the register form
    if not User.register_form_is_valid(request.form):
        return redirect("/")

    potential_user = User.find_by_email(request.form['email'])

# if user does exist redirect to loging
    if potential_user != None:
        flash("Email in use. Please log in.", "register")
        return redirect("/")

#if user does not exist then it is safe to create and hash passwword
    hashed_pw = bcrypt.generate_password_hash(request.form['password'])   
    user_data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": hashed_pw
    }
    user_id = User.register(user_data)
# saves user id in session (log them in)
    session["user_id"] = user_id
    return redirect("/facilities/all")

@app.post("/users/login")
def login():
#this route processess the register form
    if not User.login_form_is_valid(request.form):
        return redirect("/")

    potential_user = User.find_by_email(request.form['email'])
    if potential_user == None:
        flash("Invalid information", "login")
        return redirect("/")  
# user exists so no longer a potential_user
    user = potential_user
# check the password
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid information", "login")
        return redirect("/")

    session["user_id"] = user.id
    return redirect("/facilities/all")


@app.get("/users/all")
def dashboard():
#this route displays the users dashboard
    if "user_id" not in session:
        flash("You must be logged in to view that page," "login")
        return redirect("/")
    user = User.find_by_id({session['user_id']})
    return render_template("all_facilites", user=user)


@app.get("/users/logout")
def logout():
    session.clear()
    return redirect("/")
