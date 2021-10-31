from sqlalchemy.orm import relationship

from website import db


class Booking(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, nullable=False)
    book_title = db.Column(db.String(1000))
    book_author = db.Column(db.String(1000))
    book_publication_date = db.Column(db.Date)
    book_row_letter = db.Column(db.String(10))
    book_row_number = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    user_email = db.Column(db.String(1000))
    user_password = db.Column(db.String(1000))
    user_firstname = db.Column(db.String(1000))
    user_lastname = db.Column(db.String(1000))








