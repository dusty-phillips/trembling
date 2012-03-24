import cPickle as pickle
from Cookie import SimpleCookie

from mock import Mock

from trembling.session import Session, inbound


def pytest_funcarg__request(request):
    request.getfuncargvalue("mongodb")  # ensure test db is loaded
    req = Mock()
    req.cookie = SimpleCookie()
    return req


def pytest_funcarg__session(request):
    request.getfuncargvalue("mongodb")  # ensure test db is loaded
    return Session.objects.create(session_key="a" * 64)


def test_create_new_session_key(mongodb):
    t = Session.create_new_session()
    assert len(t.session_key) == 64


class TestInbound:
    def test_inbound_no_key(self, request):
        inbound(request)
        assert request.session.keys() == ["session_key"]

    def test_inbound_key_no_session(self, request):
        request.cookie['session_key'] = "a" * 64
        inbound(request)
        assert request.session.keys() == ["session_key"]

    def test_inbound_key_session(self, request, session):
        request.cookie['session_key'] = "a" * 64
        assert len(Session.objects()) == 1
        inbound(request)
        assert len(Session.objects()) == 1
        assert request.session['session_key'] == "a" * 64

    def test_inbound_loads_data(self, request, session):
        session.data = pickle.dumps({"hello": 5})
        session.save()
        request.cookie['session_key'] = "a" * 64
        inbound(request)

        assert len(Session.objects()) == 1
        assert request.session['session_key'] == "a" * 64
        assert request.session['hello'] == 5
