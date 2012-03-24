from mongoengine import connect

TEST_DB_NAME = "test_trembling_database"


def pytest_funcarg__mongodb(request):
    conn = connect(TEST_DB_NAME)

    def drop():
        conn.drop_database(TEST_DB_NAME)
    request.addfinalizer(drop)
    return conn
