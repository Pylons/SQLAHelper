Usage and API
%%%%%%%%%%%%%

Installation
============

Install SQLAHelper like any Python package, using either "pip install
SQLAHelper" or "easy_install SQLAHelper". To check out the development
repository: "hg clone http://bitbucket.org/sluggo/SQLAHelper". 

SQLAlchemy vocabulary
=====================

We can't explain all the concepts needed to use SQLAlchemy here, but a few
terms are critical for understanding SQLAHelper. To learn how to use
SQLAlchemy, see the excellent and detailed SQLAlchemy manual.

An **engine** is a SQLAlchemy object that knows how to connect to a certain
database. All SQLAlchemy applications have at least one engine.

A **session** is a SQLAlchemy object that does housekeeping for the
object-relational mapper (ORM). These sessions have nothing to do
with HTTP sessions despite the identical name. A session is required when using
the ORM, but is not needed for lower-level SQL access.

A **contextual session** (often called a **Session** with a capital S) is a
threadlocal session proxy. This means it can be a global variable in
multithreaded web servers (which may be processing different requests
simultaneously in different threads). Externally it looks like a session;
internally it maintains a separate session for each thread.  (SQLAlchemy
manual: `contextual session`_.)

A **declarative base** is a class that serves as the superclass of your ORM
classes. ORM classes correspond to database tables. SQLAlchemy has two syntaxes
for defining tables and ORM classes. A declarative base is needed only when
using the "Declarative" syntax.

Most SQLAlchemy applications nowadays use all of these.


Usage
=====

1. When your application starts up, call ``add_engine`` once for each database
   engine you will use. You will first have to create the engine using
   ``sqlalchemy.create_engine()`` or ``sqlalchemy.engine_from_config()``.
   See `Engine Configuration`_ in the SQLAlchemy manual.

2. In models or views or wherever you need them, access the contextual session,
   engines, and declarative base this way::
   
        import pyramid_sqla

        Session = pyramid_sqla.get_session()
        engine = pyramid_sqla.get_dbengine()
        Base = pyramid_sqla.get_base()

It gets slightly more complex with multiple engines as you'll see below.


API
===

.. currentmodule:: sqlahelper

.. automodule:: sqlahelper

.. autofunction:: add_engine

.. autofunction:: get_session

.. autofunction:: get_engine

.. autofunction:: get_base

.. autofunction:: reset


Examples
========

This application connects to one database. There's only one engine so we make
it the default engine. ::

    import sqlalchemy as sa
    import sqlahelper

    engine = sa.create_engine("sqlite:///db.sqlite")
    sqlahelper.add_engine(engine)

This second application is a typical Pyramid/Pylons/TurboGears application. Its
engine args are embedded in a general settings dict, which was parsed from an
application-wide INI file. All the values are strings because the INI parser is
unaware of the appropriate type for each value. ::

    import sqlalchemy as sa
    import sqlahelper

    settings = {
        "debug_notfound": "false",
        "mako.directories": "myapp:templates",
        "sqlalchemy.url": "sqlite:////home/me/applications/myapp/db.sqlite",
        "sqlalchemy.logging_name": "main",
        "sqlalchemy.pool_size": "10",
        }
    engine = sa.engine_from_config(settings, prefix="sqlalchemy.")
    sqlahelper.add_engine(engine)

The ``engine_from_config`` method finds the keys with the matching prefix,
strips the prefix, converts the values to their proper type, and calls
``add_engine`` with the extracted arguments. It ignores keys that don't have
the prefix. The only required key is the database URL ("sqlalchemy.url" in this
case).  (Note: type conversion covers only a few most common arguments.)

If ``engine_from_config`` raises "KeyError: 'pop(): dictionary is empty'", make
sure the prefix is correct. In this case it includes a trailing dot.

Multiple databases are covered in the next section.


Multiple databases
==================

A default engine plus other engines
-----------------------------------

In this scenario, the default engine is used for most operations, but two other
engines are also used occasionally::

    import sqlalchemy as sa
    import sqlahelper

    # Initialize the default engine.
    default = sa.engine_from_config(settings, prefix="sqlalchemy.")
    sqlalchelper.add_engine(default)

    # Initialize the other engines.
    engine1 = sa.engine_from_config(settings, prefix="engine1.")
    engine2 = sa.engine_from_config(settings, prefix="engine2.")
    sqlahelper.add_engine(engine1, "engine1")
    sqlahelper.add_engine(engine2, "engine2")

Queries will use the default engine by default. To use a different engine
you have to use the ``bind=`` argument on the method that executes the query;
or execute low-level SQL directly on the engine (``engine.execute(sql)``).

Two engines, but no default engine
----------------------------------

In this scenario, two engines are equally important, and neither is predominent
enough to deserve being the default engine. This is useful in applications
whose main job is to copy data from one database to another. ::

    sqlahelper.add_engine(settings, name="engine1", prefix="engine1.")
    sqlahelper.add_engine(settings, name="engine2", prefix="engine2.")

Because there is no default engine, queries will fail unless you specify an
engine every time using the ``bind=`` argument or ``engine.execute(sql)``.

Different tables bound to different engines
-------------------------------------------

It's possible to bind different ORM classes to different engines in the same
database session.  Configure your application with no default engine, and then
call the Session's ``.configure`` method with the ``binds=`` argument to
specify which classes go to which engines. For instance::

    import myapp.models as models

    sqlahelper.add_engine(engine1, "engine1")
    sqlahelper.add_engine(engine2, "engine2")
    Session = sqlahelper.get_session()
    binds = {models.Person: engine1, models.Score: engine2}
    Session.configure(binds=binds)

The keys in the ``binds`` dict can be SQLAlchemy ORM classes, table objects, or
mapper objects.


Declarative base
================

The library includes a declarative base for convenience, but some people may
choose to define their own declarative base in their model instead. And there's
one case where you *have* to create your own declarative base; namely, if you
want to modify its constructor args. The ``cls`` argument is the most common:
it specifies a superclass which all ORM object should inherit. This allows you
to define class methods and other methods which are available in all your ORM
classes.


.. _Engine Configuration: http://www.sqlalchemy.org/docs/core/engines.html
.. _contextual session: http://www.sqlalchemy.org/docs/orm/session.html#contextual-thread-local-sessions
