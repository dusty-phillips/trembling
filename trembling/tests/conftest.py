from mongoengine import connect
from trembling.auth import User

TEST_DB_NAME = "test_trembling_database"


def pytest_funcarg__mongodb(request):
    conn = connect(TEST_DB_NAME)

    def drop():
        conn.drop_database(TEST_DB_NAME)
    request.addfinalizer(drop)
    return conn


def pytest_funcarg__user(request):
    user = User(username="Paul")
    user.set_password("paul has a good password")
    user.save()
    return user
