from flask_app import app
from flask_app.models.facility import Facility #facility is the name of the class
#all of the class methods live in the the facility.py file, we are importing the entire file 
from flask_app.models.user import User
from flask import render_template, redirect, request, session, flash
from pprint import pprint


@app.get("/facilities/all")
def all_facilities():
# this route renders all the facilities
    # this checks to see if user is in session
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    facilities = Facility.find_all_with_users()
    user = User.find_by_id(session["user_id"])
    return render_template("all_facilities.html", facilities=facilities, user=user)
    # this is the template that takes all those facilities and puts them in the page, facilities=facilities sends it to the template


@app.get("/facilities/new")
def new_facility():
# this route displays the recommend a facility form
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    user = User.find_by_id(session["user_id"])
    return render_template("new_facility.html", user=user)


@app.post("/facilities/create")
def create_facility():
# this route will process the form for a new facility
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    if not Facility.form_is_valid(request.form):
        session["amenities"] = request.form["amenities"]
        return redirect("/facilities/new")

    if "amenities" in session:
        session.pop("amenities")

# down here form is valid
    Facility.create(request.form)
    return redirect("/facilities/all")


@app.get("/facilities/<int:facility_id>")
def facility_details(facility_id):
# this route displays one facility's details
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    facility = Facility.find_by_id_with_user(facility_id)
    user = User.find_by_id(session["user_id"])
    return render_template("facility_details.html", facility=facility, user=user)


@app.get("/facilities/<int:facility_id>/edit")
def edit_facility(facility_id):
# this route displays the form to edit the facility
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    facility = Facility.find_by_id_with_user(facility_id)
    user = User.find_by_id(session["user_id"])
    return render_template("edit_facility.html", facility=facility, user=user)


@app.post("/facilities/update")
def update_facility():
# this route processes the edit facility form
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    facility_id = request.form["facility_id"]  

    if not Facility.form_is_valid(request.form):
        session["amenities"] = request.form["amenities"]
        return redirect(f"/facilities/{facility_id}/edit")  


    # down here the form is valid
    if "amenities" in session:
        session.pop("amenities")
    Facility.update(request.form) #passes from the form into the facility.update
    return redirect(f"/facilities/{facility_id}")


@app.get("/facilities/<int:facility_id>/delete")
def delete_facility(facility_id):
# this route processess the delete form
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")
# can add in here if the logged in user matches the id in route
    Facility.delete(facility_id)
    return redirect("/facilities/all")