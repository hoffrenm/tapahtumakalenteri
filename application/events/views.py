from application import app, db

from application.events.models import Event
from application.events.forms import EventForm, EventModifyForm
from application.comments.models import Comment
from application.comments.forms import CommentForm
from application.auth.models import User

from flask import render_template, request, redirect, url_for, flash
from flask_security import roles_accepted, roles_required, login_required, current_user

from datetime import datetime

@app.route("/events/show/<event_id>", methods=["GET"])
@login_required
def event_show(event_id):
    event = Event.query.get(event_id)
    comments = Comment.find_comments_for_event(event_id)
    attendees = Event.participant_count(event_id)
    account = User.query.get(current_user.id)

    # format dateinfo for template
    event.day = datetime.strftime(event.date_time, '%d.')
    event.month = datetime.strftime(event.date_time,'%B')
    event.time = datetime.strftime(event.date_time, '%H:%M')
    event.date = datetime.strftime(event.date_time, '%d.%m.%Y')

    if event in account.attending:
        userHasjoined = True
    else:
        userHasjoined = False

    return render_template("events/event.html", event = event, attendees=attendees, 
                            comments=comments, form=CommentForm(), userHasjoined=userHasjoined)

@app.route("/events/join/<event_id>", methods=["POST"])
@login_required
@roles_accepted('admin', 'enduser')
def event_join(event_id):
    event = Event.query.get(event_id)
    attendees = Event.participant_count(event_id)
    account = User.query.get(current_user.id)

    # check if event has limit and has space
    if event.attendee_max > 0:
        if attendees >= event.attendee_max:
            return redirect(url_for('event_show', event_id=event.id))

    # cancel participation if user has already joined
    if event in account.attending:
        event.participants.remove(account)
        db.session().commit()
        return redirect(url_for('event_show', event_id=event.id))

    event.participants.append(account)

    db.session().commit()

    return redirect(url_for('event_show', event_id=event.id))

@app.route("/events/list/", methods=["GET"])
def events_all():
    return render_template("events/list.html", events = Event.find_all_events_attend_and_comment_count())

@app.route("/events/new/")
@login_required
@roles_required('admin')
def events_form():
    return render_template("events/new.html", form = EventForm())

@app.route("/events/own/")
@login_required
def events_own():
    events = Event.find_all_events_attend_and_comment_count_for_user(current_user.id)

    return render_template("events/list.html", events=events)

@app.route("/events/delete/<event_id>", methods=["POST"])
@login_required
@roles_required('admin')
def event_delete(event_id):
    event = Event.query.get(event_id)

    db.session().delete(event)
    db.session().commit()

    return redirect(url_for("admin_list"))

@app.route("/events/", methods=["POST"])
@login_required
@roles_required('admin')
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
  
    return redirect(url_for("events_all"))

@app.route("/events/modify/<int:event_id>", methods=["GET"])
@login_required
@roles_required('admin')
def event_edit(event_id):
    event = Event.query.get(event_id)
    
    # format time and date for prefilled form
    event.time = event.date_time.strftime('%H:%M')
    event.date = event.date_time.strftime('%Y-%m-%d')

    return render_template("events/modify.html", form = EventModifyForm(), event = event)

@app.route("/events/modify/<int:event_id>", methods=["POST"])
@login_required
@roles_required('admin')
def event_update(event_id):
    form = EventModifyForm(request.form)

    event = Event.query.get(event_id)
    
    if not event:
        return redirect(url_for("events_all"))

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

    db.session().commit()

    return redirect(url_for('admin_list'))

@app.route("/events/comment/<event_id>", methods=["POST"])
@login_required
@roles_accepted('admin', 'enduser')
def send_comment(event_id):
    form = CommentForm(request.form)
    event = Event.query.get(event_id)

    if form.validate():
        comment = Comment(form.content.data, event.id, current_user.id)

        db.session().add(comment)
        db.session().commit()
    
    return redirect(url_for('event_show', event_id=event.id))

@app.route("/events/details", methods=["GET"])
@login_required
@roles_required('admin')
def admin_list():
    events = Event.find_all_events_attend_and_comment_count()
    eventCount = db.session().query(Event).count()

    return render_template("events/adminlist.html", events = events, eventCount=eventCount)

@app.route("/events/details/<event_id>", methods=["GET"])
@login_required
@roles_required('admin')
def admin_show(event_id):
    event = Event.query.get(event_id)
    comments = Comment.find_comments_for_event(event_id)
    participants = Event.find_participants_for_event(event_id)

    return render_template("events/details.html", event = event, comments=comments, 
                            participants=participants)