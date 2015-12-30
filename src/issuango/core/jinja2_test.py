import jinja2


def test_append_once():
    l = []
    jinja2.append_once(l, 'e')

    assert l == ['e']


def test_append_twice():
    l = []
    jinja2.append_once(l, 'e')
    jinja2.append_once(l, 'e')

    assert l == ['e']
