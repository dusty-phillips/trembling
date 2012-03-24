from mongoengine import connect

def pytest_funcarg__mongodb(request):
    conn = connect("test_todoy_database")
    def drop():
        conn.drop_database("test_todoy_database")
    request.addfinalizer(drop)
    return conn