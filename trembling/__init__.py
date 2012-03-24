from aspen import Response


class Redirect(Response):
    """docstring for Redirect"""
    def __init__(self, location, code=302):
        super(Redirect, self).__init__(code)
        self.headers.set('Location', location)
