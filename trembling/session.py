import random
import string
import cPickle as pickle

from mongoengine import Document, StringField, BinaryField, OperationError

SESSION_COOKIE_NAME = "session_key"
SESSION_COOKIE_NAME_CHARACTERS = string.ascii_letters + string.digits
SESSION_COOKIE_NAME_LENGTH = 64
SESSION_COOKIE_MAX_AGE = 60 * 60 * 24 * 3


class Session(Document):
    session_key = StringField(
        max_length=SESSION_COOKIE_NAME_LENGTH,
        min_length=SESSION_COOKIE_NAME_LENGTH,
        required=True, unique=True)
    data = BinaryField()

    def __str__(self):
        return self.session_key

    @staticmethod
    def create_new_session():
        while True:
            session_key = "".join(random.choice(SESSION_COOKIE_NAME_CHARACTERS)
                for i in xrange(SESSION_COOKIE_NAME_LENGTH))

            try:
                session = Session.objects.create(session_key=session_key)
            except OperationError:  # pragma: no cover
                pass  # Key exists, Loop over to new one
            else:
                return session


# ASPEN HOOKS
def inbound(request):
    session_key = request.cookie.get('session_key')
    if session_key:
        session = Session.objects(session_key=session_key.value)
    else:
        session = None
    if session:
        session = session[0]
    else:
        session = Session.create_new_session()

    if session.data:
        data = pickle.loads(session.data)
        data["session_key"] = session.session_key
    else:
        data = {"session_key": session.session_key}

    request.session = data


def outbound(response):
    session_key = response.request.session['session_key']
    session = Session.objects(session_key=session_key)[0]
    session.data = pickle.dumps(response.request.session)
    session.save()

    response.cookie['session_key'] = response.request.session['session_key']
    response.cookie['session_key']['max-age'] = SESSION_COOKIE_MAX_AGE

