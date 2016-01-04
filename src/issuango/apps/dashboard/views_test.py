import httplib

import app


def test_index(user_client):
    assert user_client.get(app.application.reverse('index')).status_code == httplib.OK