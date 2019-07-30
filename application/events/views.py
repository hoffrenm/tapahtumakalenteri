from application import app, db
from flask import render_template, request
from application.events.models import Event

@app.route("/events/new/")
def events_form():
    return render_template("events/new.html")

@app.route("/events", methods=["GET"])
def events_index():
    return render_template("events/list.html", events = Event.query.all())

@app.route("/events/", methods=["POST"])
def events_create():
    e = Event(request.form.get("name"),
              request.form.get("location"))

    db.session().add(e)
    db.session().commit()
  
    return "hello world!"
