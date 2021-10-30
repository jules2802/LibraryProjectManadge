from flask import render_template
from flask_login import current_user

from website.views import v1

@v1.route('/home', methods=['GET', 'POST'])
def home_page():
    return render_template('home.html', user=current_user)
