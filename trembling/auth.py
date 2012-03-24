import hashlib
import string
from random import SystemRandom
random = SystemRandom()

from mongoengine import Document, StringField

from trembling.session import SESSION_COOKIE_NAME

SALT_LENGTH = 23
SALT_CHARACTERS = string.ascii_letters + string.digits
AUTH_SESSION_KEY = "auth_user_id"


class User(Document):
    username = StringField(unique=True, required=True)
    password_hash = StringField()

    def set_password(self, password):
        salt = "".join([random.choice(SALT_CHARACTERS) for x in xrange(SALT_LENGTH)])
        # FIXME: Is this secure enough?
        hasher = hashlib.sha512()
        hasher.update(salt)
        hasher.update(password)
        self.password_hash = "%s$%s" % (salt, hasher.hexdigest())

    def check_password(self, password):
        salt, hashed = self.password_hash.split("$")
        hasher = hashlib.sha512()
        hasher.update(salt)
        hasher.update(password)
        return hasher.hexdigest() == hashed


def login(request, username, password):
    '''Given a request, username, and password, authenticate the user and add
    the name to the session.

    :return True if the user is successfully authenticated, False otherwise'''
    # FIXME: Currently assumes no other user is logged in
    user = User.objects(username=username)
    if not user:
        return False
    else:
        user = user[0]

    if user.check_password(password):
        request.session[AUTH_SESSION_KEY] = username
        return True

    return False


def logout(request):
    '''Ensure that no user session data is attached to the request.'''
    key = request.session[SESSION_COOKIE_NAME]
    request.session = {SESSION_COOKIE_NAME: key}


def inbound(request):
    '''Attach a User object to every request if the user id is logged in'''
    request.user = None
    request.authenticated = False
    if 'auth_user_id' in request.session:
        user = User.objects(username=request.session[AUTH_SESSION_KEY])
        if user:
            request.user = user[0]
            request.authenticated = True
