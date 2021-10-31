from flask import request, render_template, flash, url_for, redirect
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

import app
from website import db
from website.models.user import User
from website.views.interface import v1


@v1.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form['email']
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        password1 = request.form['password1']
        password2 = request.form['password2']
        special_access = request.form['specialAccess']

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address alreadu registered', category='error')

        elif len(first_name) == 0:
            flash('First name missing', category='error')

        elif len(last_name) == 0:
            flash('Last name missing', category='error')

        elif len(password1) == 0:
            flash('Password missing', category='error')

        elif password1 != password2:
            flash('Passwords do not match', category='error')

        elif len(special_access) is not 0 and special_access != app.app.config['SECRET_KEY']:
            flash('Special password is incorrect', category='error')

        elif len(special_access) is not 0:
            new_user = User(email=email, firstname=first_name, lastname=last_name,
                            password=generate_password_hash(password1, method='sha256'), special_access=True)
            db.session.add(new_user)
            db.session.commit()
            flash('New user with special access registered')
            return redirect((url_for('v1.login')))
        else:
            new_user = User(email=email, firstname=first_name, lastname=last_name,
                            password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('New user registered', category='success')
            return redirect(url_for('v1.login'))

        return render_template('sign_up.html', user=current_user), 400

    if request.method=='GET':
        return render_template('sign_up.html', user=current_user), 200


@v1.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password=password):
                login_user(user, remember=True)
                flash('You logged in successfully', category='success')
                return redirect(url_for('v1.home_page'))
                
            else:
                flash('Incorrect password', category='error')
        else:
            flash('This email is not linked to an account', category='error')

        return render_template('login.html', user=current_user), 400

    if request.method == 'GET':
        return render_template('login.html', user=current_user)

@v1.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been looged out', category='success')
    return redirect(url_for('v1.login'))

