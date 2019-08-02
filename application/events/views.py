from application import app, db
from flask import render_template, request, redirect, url_for
from application.events.models import Event
from application.events.forms import EventForm, EventModifyForm
from datetime import datetime

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

    e.date_time = datetime.combine(form.date.data, form.time.data)
    e.attendee_max = form.attendee_max.data
    e.attendee_min = form.attendee_min.data

    db.session().add(e)
    db.session().commit()
  
    return redirect(url_for("events_index"))

# Show prefilled modification form
@app.route("/events/modify/<event_id>", methods=["GET"])
def event_show_modify(event_id):
    event = Event.query.get(event_id)

    return render_template("events/modify.html", form = EventModifyForm(), event = event)

@app.route("/events/modify/<event_id>", methods=["POST"])
def event_modify(event_id):
    return "lol"
    
