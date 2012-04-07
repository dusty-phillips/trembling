TREMBLING ASPEN
===============

This module contains some standard web framework functionality intended to integrate with the [Aspen](http://aspen.io/) web framework. Aspen does not currently include these features, so I've created basic implementations of them:

* Sessions
* Single Request Messages
* Authentication

The session and auth implementations use mongo_engine for storage. To use them, ensure
trembling is on your path and make your Aspen
[hooks.conf](http://aspen.io/hooks/) look something like this:

    # Startup Hooks
    database:startup

    ^L
    # Inbound Early Hooks
    trembling.session:inbound
    trembling.auth:inbound

    ^L
    # Inbound Late Hooks

    ^L
    # Outbound Early hooks

    ^L
    # Outbound Late Hooks
    trembling.session:outbound

    ^L
    # Shutdown Hooks


This assumes your project has a .aspen/database.py (you can change the startup
hook if you prefer a different filename) to configure the database. At a bare
minimum it'll look something like this:
    
    from mongoengine import connect

    def startup(website):
        website.db = connect("MY_DB_NAME")

Authenticating
--------------
There is a `trembling.auth.User` mongoengine document that you can use
to access user data. The auth module also contains login, logout, and login_required methods. Call them from your simplate as

* login(request, username, password)
* logout(request)
* login_required(request, "/login/page.html")

The latter will raise an appropriate redirect response if the user is not
authenticated. If you do not specify a redirect url, it will redirect to
trembling.auth.LOGIN_URL. This defaults to /account/login.html, or you can set
it to a string of your choice in an aspen startup hook.

For an example of how these modules can be used in practice, see
[Todoy](https://github.com/buchuki/Todoy)

Messages
--------
If you put something in request.session['messages'] it will automatically be
popped and submitted as request.messages in the following request. Note that
it doesn't currently do any handling of combining multiple messages into a list
or anything like that.

TESTING
-------

Testing requires py.test, and optionally, for code coverage, 
coverage.py and pytest-cov. I have the following in my .bashrc:

py.test --cov=. --cov-report=html --cov-config=coveragerc

TODO
----

I'd like to remove the dependency on mongoengine by creating a pluggable session backend engine as is used in Django.

I'm not sure how secure this code is. I took web.py and Django
as input, but I've only implemented the bare minimum.

Pull requests are always welcome!