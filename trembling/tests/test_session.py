from trembling.session import Session
from ludibrio import Stub


def test_get_new_session_key(mongodb):
    t = Session.create_new_session()
    assert len(t.session_key) == 64
