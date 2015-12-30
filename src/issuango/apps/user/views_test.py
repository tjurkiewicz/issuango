import httplib

import app

def test_sign_in(client):
    assert client.get(app.application.reverse('sign-in')).status_code == httplib.OK


def test_sign_in_already_authorized(admin_client):
    assert admin_client.get(app.application.reverse('sign-in')).status_code == httplib.FOUND


def test_sign_out(admin_client):
    assert admin_client.get(app.application.reverse('sign-out')).status_code == httplib.FOUND
