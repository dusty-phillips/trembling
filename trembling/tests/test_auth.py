from trembling.auth import User, inbound, login, logout
from mock import Mock
from aspen import Response


def pytest_funcarg__request(request):
    request = Mock()
    request.session = {"session_key": "a" * 64}
    return request


def test_password_hash_match(mongodb):
    user = User()
    user.username = "Paul"
    user.set_password("ice cream rocks")
    assert user.check_password("ice cream rocks") == True
    assert user.check_password("fish socks win") == False


def test_inbound_nouser(mongodb, request):
    request = Mock()
    request.session = {"session_key": "a" * 64}
    inbound(request)
    assert request.user == None
    assert request.authenticated == False


def test_inbound_user(mongodb, user, request):
    request.session['auth_user_id'] = "Paul"
    inbound(request)
    assert request.user == user
    assert request.authenticated == True


def test_inbound_user_notexists(mongodb, request):
    request.session['auth_user_id'] = "Paul"
    inbound(request)
    assert request.user == None
    assert request.authenticated == False


def test_login_success(mongodb, user, request):
    assert login(request, "Paul", "paul has a good password")
    assert request.session['auth_user_id'] == "Paul"


def test_login_fail(mongodb, user, request):
    assert not login(request, "Paul", "paul has a bad password")
    assert 'auth_user_id' not in request.session


def test_login_user_not_exist(mongodb, user, request):
    assert not login(request, "Edgar", "edgar doesnt exist")
    assert 'auth_user_id' not in request.session


def test_logout(mongodb, user, request):
    login(request, "Paul", "paul has a good password")
    session_key = request.session['session_key']
    request.session['paulsdata'] = "something secret and important"
    logout(request)
    assert request.session == {'session_key': session_key}
