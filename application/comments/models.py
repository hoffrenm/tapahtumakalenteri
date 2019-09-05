from application import db

from sqlalchemy.sql import text

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp())

    content = db.Column(db.String(144), nullable=False)

    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    
    def __init__(self, content, event_id, account_id):
        self.content = content
        self.event_id = event_id
        self.account_id = account_id

    # find comments and authors for single event view
    def find_comments_for_event(event_id):
        stmt = text("SELECT Account.name, Comment.content, Comment.date_created,"
                    " Comment.account_id, Comment.id"
                    " FROM Comment"
                    " LEFT JOIN Account ON Comment.account_id = Account.id"
                    " WHERE Comment.event_id = :event_id"
                    " ORDER BY Comment.date_created ASC").params(event_id=event_id)
        
        res = db.engine.execute(stmt)

        response = []

        for row in res:
            response.append({"name":row[0], "content":row[1], "date":row[2],
                            "accountId":row[3], "id":row[4]})

        return response
