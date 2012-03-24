from trembling.shortcuts import Redirect

def test_redirect():
    response = Redirect("/")
    assert response.code == 302
    assert response.headers.one("Location") == "/"