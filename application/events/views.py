from application import app, db
from application.events.models import Event
from application.auth.models import User
from application.events.forms import EventForm, EventModifyForm

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from datetime import datetime

@app.route("/events/show/<int:event_id>", methods=["GET"])
def event_show(event_id):
    event = Event.query.get(event_id)
    return render_template("events/event.html", event = event)


@app.route("/events/join/<event_id>", methods=["POST"])
@login_required
def event_join(event_id):
    event = Event.query.get(event_id)
    account = User.query.get(current_user.id)

    # check if event has limit and has space
    if event.attendee_max > 0:
        if event.attendees >= event.attendee_max:
            return "Tapahtumassa ei ollut tilaa"

    # check if user has already joined an event
    if event in account.attending:
        flash("Olet jo ilmottautunut")
        return "Olet jo ilmottautunut"

    event.participants.append(account)

    db.session.commit()

    return redirect(url_for("events_index"))

@app.route("/events/", methods=["GET"])
def events_index():
    return render_template("events/list.html", events = Event.query.all())

@app.route("/events/new/")
@login_required
def events_form():
    return render_template("events/new.html", form = EventForm())

@app.route("/events/", methods=["POST"])
@login_required
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

@app.route("/events/modify/<int:event_id>", methods=["GET"])
@login_required
def event_edit(event_id):
    event = Event.query.get(event_id)
    
    # format time and date for prefilled form
    event.time = event.date_time.strftime('%H:%M')
    event.date = event.date_time.strftime('%Y-%m-%d')

    return render_template("events/modify.html", form = EventModifyForm(), event = event)


@app.route("/events/modify/<int:event_id>", methods=["POST"])
@login_required
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
    
