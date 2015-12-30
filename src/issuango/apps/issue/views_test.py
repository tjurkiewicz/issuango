import httplib

import app
import issuango.apps.user.app


def test_create_not_signed_in(client):
    response = client.get(app.application.reverse('create'))
    assert response.status_code == httplib.FOUND
    assert response.url.startswith(issuango.apps.user.app.application.reverse('sign-in'))


def test_create_no_projects(user_client):
    response = user_client.get(app.application.reverse('create'))
    assert response.status_code == httplib.FOUND
    assert response.url.startswith(app.application.reverse('no-projects'))

