from datetime import datetime

from flask import render_template, request, flash
from flask_login import current_user, login_required
from sqlalchemy import Date

from website import db
from website.models.book import Book
from website.views import v1


@v1.route('/home', methods=['GET', 'POST'])
def home_page():
    return render_template('home.html', user=current_user)


@v1.route('/add-book', methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':

        title = request.form['title']
        author = request.form['author']
        print(request.form.get('publicationDate'))
        publication_date = request.form.get('publicationDate')
        row_letter = request.form['rowLetter'].upper()
        row_number = request.form['rowNumber']

        print(request.form)

        if (len(title) is 0) or (len(author) is 0) or (len(row_letter) is 0) or (len(row_number) is 0) or (
                publication_date is ''):
            flash("A field is missing", category='error')

        elif Book.query.filter_by(row_letter=row_letter, row_number=row_number).first():
            flash("Book location is already taken", category='error')
        else:

            publication_date = datetime.strptime(publication_date, '%Y-%m-%d')
            availability = publication_date < datetime.today()

            new_book = Book(title=title, author=author, publication_date=publication_date, row_letter=row_letter,
                            row_number=row_number, available=availability)
            db.session.add(new_book)
            db.session.commit()
            flash('A new book has been add to the library')


    inventory = Book.query.all()

    return render_template('add_book.html', inventory=inventory, user=current_user)
