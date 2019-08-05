from application import app, db
from flask import render_template, request, redirect, url_for
from application.events.models import Event
from application.events.forms import EventForm, EventModifyForm
from datetime import datetime

@app.route("/events", methods=["GET"])
def events_index():
    return render_template("events/list.html", events = Event.query.all())

@app.route("/events/new")
def events_form():
    return render_template("events/new.html", form = EventForm())

@app.route("/events", methods=["POST"])
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

# pass event to form so it can be prefilled
@app.route("/events/modify/<int:event_id>", methods=["GET"])
def event_edit(event_id):
    event = Event.query.get(event_id)
    
    # format time and date for prefilled form
    event.time = event.date_time.strftime('%H:%M')
    event.date = event.date_time.strftime('%Y-%m-%d')

    return render_template("events/modify.html", form = EventModifyForm(), event = event)


@app.route("/events/modify/<int:event_id>", methods=["POST"])
def event_update(event_id):
    form = EventModifyForm(request.form)

    event = Event.query.get(event_id)
    
    # format time and date for prefilled form
    event.time = event.date_time.strftime('%H:%M')
    event.date = event.date_time.strftime('%Y-%m-%d')

    if not form.validate():
        return render_template("events/modify.html", form = form, event = event)

    event.name = form.name.data
    event.location = form.location.data
    event.date_time = datetime.combine(form.date.data, form.time.data)
    event.attendee_max = form.attendee_max.data
    event.attendee_min = form.attendee_min.data

    db.session.commit()

    return redirect(url_for("events_index"))
    
