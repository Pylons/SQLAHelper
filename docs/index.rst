SQLAHelper
==========
:Version: 1.0, released 2011-12-25
:PyPI: http://pypi.python.org/pypi/SQLAHelper
:Docs: http://sluggo.scrapping.cc/python/SQLAHelper/
:Source: http://bitbucket.org/sluggo/sqlahelper (Mercurial)


**SQLAHeler** is a small library for SQLAlchemy_ web applications. It acts as a
container for the application's contextual session, engines, and declarative
base. This avoids circular dependencies between the application's model
modules, and allows cooperating third-party libraries to use the application's
session, base, and transaction. SQLAHelper does not try to hide or disguise the
underlying SQLAlchemy objects; it merely provides a way to organize them.

The contextual session is initialized with the popular
ZopeTransactionExtension, which allows it to work with transaction managers
like pyramid_tm_ and repoze.tm2_. A transaction manager provides automatic
commit at the end of request processing, or rollback if an exception is raised
or HTTP error status occurs. Some transaction managers can commit both SQL and
non-SQL actions in one step. SQLAHelper does not include a transaction manager,
but it works with the most common ones.

It's currently tested on Python 2.7/Linux but should work on other
platforms. A set of unit tests is included. Python 3 compatibility is unknown
but will be addressed soon.


.. _SQLAlchemy: http://sqlalchemy.org/
.. _Pyramid: http://docs.pylonshq.com/pyramid/dev/

.. _zope.sqlalchemy: http://pypi.python.org/pypi/zope.sqlalchemy
.. _contextual session: http://www.sqlalchemy.org/docs/orm/session.html#contextual-thread-local-sessions
.. _repoze.tm2: http://docs.repoze.org/tm2/
.. _transaction: http://pypi.python.org/pypi/transaction
.. _pyramid_tm: http://pypi.python.org/pypi/pyramid_tm


Documentation
-------------

.. toctree::
   :maxdepth: 1

   usage
   changes
