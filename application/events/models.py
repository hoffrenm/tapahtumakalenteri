from application import db

from sqlalchemy.sql import text

attends = db.Table('participation',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id', ondelete="CASCADE")),
    db.Column('account_id', db.Integer, db.ForeignKey('account.id', ondelete="CASCADE"))
)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp())

    name = db.Column(db.String(144), nullable=False)
    location = db.Column(db.String(144), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    attendee_max = db.Column(db.Integer, default=0)
    attendee_min = db.Column(db.Integer, default=0)

    participants = db.relationship("User", secondary=attends, backref=db.backref("attending", lazy="dynamic"))

    # declare relationship between event and comment so 
    # removal of an event causes deletion of all related comments
    comments = db.relationship("Comment", cascade="all, delete", backref="comment")

    def __init__(self, name, location):
        self.name = name
        self.location = location

    def find_participants_for_event(event_id):
        stmt = text("SELECT Account.name"
                    " FROM Account"
                    " LEFT JOIN Participation ON Participation.account_id = Account.id"
                    " WHERE Participation.event_id = :event_id").params(event_id=event_id)
        
        res = db.engine.execute(stmt)

        response = []

        for row in res:
            response.append({"name":row[0]})

        return response

    # query for list view. Includes information for event and number of 
    # comments and participants for specific event
    def find_all_events_attend_and_comment_count():
        stmt = text("SELECT Event.id, Event.name, Event.location,"
                    " COUNT(DISTINCT Comment.id), COUNT(DISTINCT Participation.account_id)"
                    " FROM Event"
                    " LEFT JOIN Comment ON Comment.event_id = Event.id"
                    " LEFT JOIN Participation ON Participation.event_id = Event.id"
                    " GROUP BY Event.id"
                    " ORDER BY Event.date_time ASC")

        res = db.engine.execute(stmt)

        response = []

        for row in res:
            response.append({"id":row[0], "name":row[1], "location":row[2],
                             "commentCount":row[3], "attendeeCount":row[4]})

        return response

    def find_all_events_attend_and_comment_count_for_user(account_id):
        stmt = text("SELECT Event.id, Event.name, Event.location,"
                    " COUNT(DISTINCT Comment.id), COUNT(DISTINCT Participation.account_id)"
                    " FROM Event"
                    " LEFT JOIN Comment ON Comment.event_id = Event.id"
                    " LEFT JOIN Participation ON Participation.event_id = Event.id"
                    " WHERE Participation.event_id IN "
                    " ( "
                    "   SELECT Event.id "
                    "       FROM Event "
                    "       LEFT JOIN Participation ON Participation.event_id = Event.id "
                    "       WHERE Participation.account_id = :account_id "
                    " ) "
                    " GROUP BY Event.id"
                    " ORDER BY Event.date_time ASC").params(account_id=account_id)

        res = db.engine.execute(stmt)

        response = []

        for row in res:
            response.append({"id":row[0], "name":row[1], "location":row[2],
                             "commentCount":row[3], "attendeeCount":row[4]})

        return response

    def participant_count(event_id):
        stmt = text("SELECT COUNT(*) FROM Participation"
                    " JOIN Event ON Participation.event_id = Event.id"
                    " WHERE Event.id = :event_id").params(event_id=event_id)

        res = db.engine.execute(stmt)

        return res.scalar()
