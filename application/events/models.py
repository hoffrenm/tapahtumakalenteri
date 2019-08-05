from application import db

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

    def __init__(self, name, location):
        self.name = name
        self.location = location

