TREMBLING ASPEN
===============

These are session and authentication modules for the [Aspen](http://aspen.io/) web framework.
They use mongo_engine for storage. To use, ensure trembling is on your path and make
your Aspen [hooks.conf](http://aspen.io/hooks/) look something like this:

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