from application import app, db
from flask import render_template, request, redirect, url_for
from application.events.models import Event
from application.events.forms import EventForm

@app.route("/events/new/")
def events_form():
    return render_template("events/new.html", form = EventForm())

@app.route("/events", methods=["GET"])
def events_index():
    return render_template("events/list.html", events = Event.query.all())

@app.route("/events/", methods=["POST"])
def events_create():
    form = EventForm(request.form)

    if not form.validate():
        return render_template("events/new.html", form = form)

    e = Event(form.name.data, form.location.data)

    db.session().add(e)
    db.session().commit()
  
    return redirect(url_for("events_index"))
