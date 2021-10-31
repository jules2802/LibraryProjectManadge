from datetime import datetime
from flask import render_template, request, flash, Blueprint
from flask_login import current_user, login_required

from website import db
from website.models.book import Book, location_is_used


v1 = Blueprint('v1', __name__)

@v1.route('/home', methods=['GET', 'POST'])
def home_page():
    return render_template('home.html', user=current_user)


@v1.route('/add-book', methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':

        title = request.form['title']
        author = request.form['author']
        publication_date = request.form.get('publicationDate')
        row_letter = request.form['rowLetter'].upper()
        row_number = request.form['rowNumber']


        if (len(title) is 0) or (len(author) is 0) or (len(row_letter) is 0) or (len(row_number) is 0) or (
                publication_date is ''):
            flash("A field is missing", category='error')

        elif row_letter.isalpha() is False:
            flash("Book row letter should contain only letters", category='error')

        elif location_is_used(row_letter,row_number):
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

@v1.route('/change-location', methods=['GET','POST'])
def change_location():
    if request.method=='POST':
        row_letter = request.form['rowLetter']
        row_number = request.form['rowNumber']

        if (len(row_letter) is 0) or (len(row_number) is 0):
            flash("An input is missing")

        elif row_letter.isalpha() is False:
            flash('Row letter input should contain only letters', category='error')

        elif location_is_used(row_letter, row_number):
            flash('Location is already used', category='error')
        else:
            id_book = request.form['book']
            book = Book.query.filter_by(id=id_book).first()
            book.row_letter = row_letter
            book.row_number = row_number
            db.session.commit()
            flash('Book location has been correctly updated')

            ##Faire en sorte qu'on ne puisse pas remettre le meme emplacement
    inventory = Book.query.all()
    return render_template('book_location.html', inventory=inventory, user=current_user)

