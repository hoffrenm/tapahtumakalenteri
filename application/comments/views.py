from application import app, db

from application.comments.models import Comment
from application.comments.forms import CommentForm, CommentEditForm
from application.auth.models import User

from flask import render_template, redirect, request, url_for
from flask_security import roles_accepted, roles_required, login_required, current_user

@app.route("/comments/modify/<comment_id>", methods=["GET", "POST"])
@login_required
@roles_accepted('admin', 'enduser')
def comment_edit(comment_id):
    comment = Comment.query.get(comment_id)

    if request.method == "GET":
        return render_template("comments/edit.html", form=CommentEditForm(), comment=comment)

    form = CommentEditForm(request.form)

    # allow admin and author of comment to modify it
    if current_user.has_role('admin') or current_user.id == comment.account_id:
        if form.validate():
            comment.content = form.content.data

            db.session().commit()
    
    if current_user.has_role('admin'):
        return redirect(url_for('admin_show', event_id=comment.event_id))

    return redirect(url_for('event_show', event_id=comment.event_id))

@app.route("/comments/delete/<comment_id>", methods=["POST"])
@login_required
@roles_accepted('admin', 'enduser')
def comment_delete(comment_id):
    comment = Comment.query.get(comment_id)

    # allow admin and author of comment to delete it
    if current_user.has_role('admin'):
        db.session().delete(comment)
        db.session().commit()
        return redirect(url_for('admin_show', event_id=comment.event_id))
    elif current_user.id == comment.account_id:
        db.session().delete(comment)
        db.session().commit()
        return redirect(url_for('event_show', event_id=comment.event_id))
    
    return redirect(url_for('events_all'))

@app.route("/comments/new/")
@login_required
@roles_required('admin')
def comment_edit_form():
    return render_template("events/new.html", form = EventForm())