SQLAHelper
==========
:Version: 1.0b1, released 2010-03-11
:PyPI: http://pypi.python.org/pypi/SQLAHelper
:Docs: https://bitbucket.org/sluggo/sqlahelper/wiki/html/index.html
:Source: http://bitbucket.org/sluggo/sqlahelper (Mercurial)


**SQLAHeler** is a small library for SQLAlchemy_ web applications. It acts as a
container for the application's contextual session, engines, and declarative
base. This avoids circular dependencies or the need for a 'meta' module if your
model is split across multiple modules. SQLAHelper does not try to hide the
underlying SQLAlchemy objects; it merely provides a way to organize them and
some convenience functions for initializing them.

The contextual session can be used with transaction managers (it's initialized
with the ZopeTransactionExtension, as TurboGears has long done). A transaction
manager provides automatic commit at the end of request processing, or rollback
if an exception or HTTP error status occurred. SQLAHelper does not include any
transaction managers, but it's known to work with repoze.tm2_, which is
middleware and should work with any WSGI framework, and pyramid_tm_ which is
specific to Pyramid.

Version 1.0b1 is a public beta test before the final release. We want to try it
in real applications before making it final.

It's currently tested on Python 2.6/Linux but should
work on 2.5 and other platforms. A set of unit tests is included.

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
   model_examples
   bugs
   changes

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

