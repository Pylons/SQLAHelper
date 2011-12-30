import sqlalchemy as sa
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm
from zope.sqlalchemy import ZopeTransactionExtension

# Import only version 1 API with "import *"
__all__ = ["add_engine", "get_base", "get_session", "get_engine"]

# VERSION 2 API

class AttributeContainer(object):
    def _clear(self):
        """Delete all instance attributes. For internal use only."""
        self.__dict__.clear()

engines = AttributeContainer()
bases = AttributeContainer()
sessions = AttributeContainer()

_zte = ZopeTransactionExtension()

def set_default_engine(engine):
    engines.default = engine
    bases.default.metadata.bind = engine
    sessions.default.configure(bind=engine)

def reset():
    """Restore the initial module state, deleting all modifications.
    
    This function is mainly for unit tests and debugging. It undoes all
    customizations and reverts to the initial module state.
    """
    engines._clear()
    bases._clear()
    sessions._clear()
    engines.default = None
    bases.default = declarative.declarative_base()
    sm = orm.sessionmaker(extension=[_zte])
    sessions.default = orm.scoped_session(sm)

reset()

# VERSION 1 API

def add_engine(engine, name="default"):
    """Add a SQLAlchemy engine to the engine repository.

    The engine will be stored in the repository under the specified name, and
    can be retrieved later by calling ``get_engine(name)``.

    If the name is "default" or omitted, this will be the application's default
    engine. The contextual session will be bound to it, the declarative base's
    metadata will be bound to it, and calling ``get_engine()`` without an
    argument will return it.
    """
    if name == "default":
        set_default_engine(engine)
    else:
        setattr(engines, name, engine)

def get_session():
    """Return the central SQLAlchemy contextual session.
    
    To customize the kinds of sessions this contextual session creates, call
    its ``configure`` method::

        sqlahelper.get_session().configure(...)

    But if you do this, be careful about the 'ext' arg. If you pass it, the
    ZopeTransactionExtension will be disabled and you won't be able to use this
    contextual session with transaction managers. To keep the extension active
    you'll have to re-add it as an argument. The extension is accessible under
    the semi-private variable ``_zte``. Here's an example of adding your own
    extensions without disabling the ZTE::

        sqlahelper.get_session().configure(ext=[sqlahelper._zte, ...])
    """
    return sessions.default

def get_engine(name="default"):
    """Look up an engine by name in the engine repository and return it.

    If no argument, look for an engine named "default".

    Raise ``RuntimeError`` if no engine under that name has been configured.
    """
    try:
        return getattr(engines, name)
    except AttributeError:
        raise RuntimeError("No engine '%s' was configured" % name)

def get_base():
    """Return the central SQLAlchemy declarative base.
    """
    return bases.default

def set_base(base):
    """Set the central SQLAlchemy declarative base.

    Subsequent calls to ``get_base()`` will return this base instead of the
    default one. This is useful if you need to override the default base, for
    instance to make it inherit from your own superclass.

    You'll have to make sure that no part of your application's code or any
    third-party library calls ``get_base()`` before you call ``set_base()``,
    otherwise they'll get the old base. You can ensure this by calling
    ``set_base()`` early in the application's execution, before importing the
    third-party libraries.
    """
    bases.default = base
