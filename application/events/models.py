from application import db

from sqlalchemy.sql import text

attends = db.Table('participation',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
    db.Column('account_id', db.Integer, db.ForeignKey('account.id'))
)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp())

    name = db.Column(db.String(144), nullable=False)
    location = db.Column(db.String(144), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    attendees = db.Column(db.Integer, default=0)
    attendee_max = db.Column(db.Integer, default=0)
    attendee_min = db.Column(db.Integer, default=0)

    participants = db.relationship("User", secondary=attends, backref=db.backref("attending", lazy="dynamic"))

    def __init__(self, name, location):
        self.name = name
        self.location = location

    def find_comments_for_event(event_id):
        stmt = text("SELECT Account.name, Comment.content, Comment.date_created"
                    " FROM Comment"
                    " LEFT JOIN Account ON Comment.account_id = Account.id"
                    " WHERE Comment.event_id = :event_id"
                    " ORDER BY Comment.date_created ASC").params(event_id=event_id)
        
        res = db.engine.execute(stmt)

        response = []

        for row in res:
            response.append({"name":row[0], "content":row[1], "date":row[2]})

        return response

