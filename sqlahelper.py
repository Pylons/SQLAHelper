import sqlalchemy as sa
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm
from zope.sqlalchemy import ZopeTransactionExtension

# Global variables initialized by ``reset()``.
_base = _session = _engines = _zte = None

def reset():
    """Delete all engines and restore the initial module state.
    
    This function is mainly for unit tests and debugging. It undoes all
    customizations and reverts to the initial module state.
    """
    global _base, _session, _engines, _zte
    _zte = ZopeTransactionExtension()
    sm = orm.sessionmaker(extension=[_zte])
    _base = declarative.declarative_base()
    _session = orm.scoped_session(sm)
    _engines = {}

reset()

# PUBLIC API

__all__ = [
    "add_engine", 
    "get_base",
    "get_session", 
    "get_engine",
    ]
    # "reset" is not included because it's not intended for normal use.

def add_engine(engine, name="default"):
    """Add a SQLAlchemy engine to the engine repository.

    The engine will be stored in the repository under the specified name, and
    can be retrieved later by calling ``get_engine(name)``.

    If the name is "default" or omitted, this will be the application's default
    engine. The contextual session will be bound to it, the declarative base's
    metadata will be bound to it, and calling ``get_engine()`` without an
    """
    _engines[name] = engine
    if name == "default":
        _session.configure(bind=engine)
        _base.metadata.bind = engine

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
    return _session

def get_engine(name="default"):
    """Look up an engine by name in the engine repository and return it.

    If no argument, look for an engine named "default".

    Raise ``RuntimeError`` if no engine by the specified was configured.
    """
    try:
        return _engines[name]
    except KeyError:
        raise RuntimeError("No engine '%s' was configured" % name)

def get_base():
    """Return the central SQLAlchemy declarative base.
    """
    return _base
