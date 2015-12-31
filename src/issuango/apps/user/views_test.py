import httplib

import django.conf

import app
import views
import issuango.apps.dashboard.app


def test_sign_in(client):
    assert client.get(app.application.reverse('sign-in')).status_code == httplib.OK


def test_do_sign_in_success(client, user):
    next = 'something'
    url = '{}?{}={}'.format(app.application.reverse('sign-in'), views.SignInView.redirect_field_name, next)

    response = client.post(url, {'username': user.username, 'password': 'password', 'remember': False})
    assert response.status_code == httplib.FOUND
    assert response.url == next


def test_sign_in_already_authorized(user_client):
    response = user_client.get(app.application.reverse('sign-in'))
    assert response.url == django.conf.settings.LOGIN_REDIRECT_URL
    assert response.status_code == httplib.FOUND


def test_sign_out(user_client):
    response = user_client.get(app.application.reverse('sign-out'))
    assert response.url == issuango.apps.dashboard.app.application.reverse('index')
    assert response.status_code == httplib.FOUND

