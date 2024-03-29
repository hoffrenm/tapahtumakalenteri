from application import app, db, user_datastore
from application.auth.models import User, Role
from application.auth.forms import LoginForm, AccountCreateForm

from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from flask_security import roles_accepted, roles_required, login_required, current_user

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)

    user = User.query.filter_by(username=form.username.data, password=form.password.data).first()

    if not user:
        return render_template("auth/loginform.html", form = form,
                                error = "No such username or password")

    login_user(user)
    return redirect(url_for("index"))

@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/auth/register", methods = ["GET"])
def show_register():
    return render_template("auth/accountform.html", form = AccountCreateForm())

@app.route("/auth/register", methods = ["POST"])
def register():
    form = AccountCreateForm(request.form)

    if not form.validate():
        return render_template("auth/accountform.html", form = form)

    user = User.query.filter_by(username=form.username.data).first()

    if user:
        form.username.errors.append("Käyttäjätunnus on jo käytössä")
        return render_template("auth/accountform.html", form = form)

    enduser = Role.query.filter_by(name='enduser').first()

    u = User(form.name.data, form.username.data, form.password.data)
    u.roles.append(enduser)

    db.session().add(u)
    db.session().commit()

    return redirect(url_for("events_all"))

@app.route("/users", methods = ["GET"])
@login_required
@roles_required('admin')
def users():
    users = User.find_users_comments_and_participations()
    roles = User.find_roles_count()
    userCount = db.session.query(User).count()

    return render_template("auth/users.html", users=users, userCount=userCount, roles=roles)
