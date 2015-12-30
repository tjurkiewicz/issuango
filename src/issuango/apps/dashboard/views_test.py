import httplib

import app


def test_index(client):
    assert client.get(app.application.reverse('index')).status_code == httplib.OK