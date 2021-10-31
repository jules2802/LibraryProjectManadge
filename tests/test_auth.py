import os
import tempfile

import pytest
from flask import Flask

from app import app
from website import create_app
from website.models.user import User
from website.views.interface import v1


@pytest.fixture
def client():
    app.config['TESTING'] =True
    with app.test_client() as client:
        yield client


def test_1(client):

    sign_in_form = {
        'email': 'jules@jules.fr',
        'firstName': 'juleeees',
        'lastName': 'eee',
        'password1': 'bonjour',
        'password2': 'bonjour',
        'specialAccess': "Manadge project"}

    response = client.post('/sign-up', data=sign_in_form)
    user = User.query.filter_by().first()


    assert user is not None
    assert user.firstname =='jules'

    assert response.status_code == 200
