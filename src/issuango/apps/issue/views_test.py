import httplib

import issuango.apps.user.app

import app
import models



def test_create_not_signed_in(client):
    response = client.get(app.application.reverse('issue-create'))
    assert response.status_code == httplib.FOUND
    assert response.url.startswith(issuango.apps.user.app.application.reverse('sign-in'))


def test_create_no_projects(user_client):
    response = user_client.get(app.application.reverse('issue-create'))
    assert response.status_code == httplib.FOUND
    assert response.url.startswith(app.application.reverse('no-projects'))


def test_create(user_client, role):
    r = role(models.ProjectRole.READ_ROLE)

    response = user_client.get(app.application.reverse('issue-create'))
    assert response.status_code == httplib.OK

