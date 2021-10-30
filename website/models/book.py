from website import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    author = db.Column(db.String(1000))
    publication_date = db.Column(db.Date)
    row_letter = db.Column(db.String(10))
    row_number = db.Column(db.Integer)
    available = db.Column(db.Boolean, default=False)


