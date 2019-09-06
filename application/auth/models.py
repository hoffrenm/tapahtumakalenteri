from application import db

from flask_security import RoleMixin, UserMixin
from sqlalchemy.sql import text

roles_users = db.Table('roles_users',
    db.Column('account_id', db.Integer(), db.ForeignKey('account.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    
    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)

    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    # queries for all users and counts their comments and participations to events
    def find_users_comments_and_participations():
        stmt = text("SELECT Account.name, COUNT(DISTINCT Comment.id), COUNT(DISTINCT Participation.event_id)"
                    " FROM Account"
                    " LEFT JOIN Comment ON Comment.account_id = Account.id"
                    " LEFT JOIN Participation ON Participation.account_id = Account.id"
                    " GROUP BY Account.name")

        res = db.engine.execute(stmt)

        response = []

        for row in res:
            response.append({"name":row[0], "commentCount":row[1], "eventCount":row[2]})

        return response

    def find_roles_count():
        stmt = text("SELECT Role.name, COUNT(Roles_users.account_id)"
                    " FROM Role"
                    " LEFT JOIN Roles_users ON Roles_users.role_id = Role.id"
                    " GROUP BY Role.name")

        res = db.engine.execute(stmt)

        response = []

        for row in res:
            response.append({"name":row[0], "roleCount":row[1] })

        return response
    