SQLAHelper is a small library for SQLAlchemy web applications. It was written
for Pyramid but is not framework-specific. It acts as a container for the
application's contextual session, engines, and declarative base. This avoids
circular dependencies between the application's model modules, and allows
cooperating third-party libraries to use the session, base, and transaction.

The contextual session is initialized with the ZopeTransactionExtension so that
it can be used with transaction managers. This can be disabled if desired.

It's currently tested on Python 2.7/Linux but should work on 2.5 and other
platforms. A set of unit tests is included. Python 3 compatibility is unknown
but will be addressed soon.

Documentation is in the 'docs' directory.

(c) 2010-2011 Mike Orr
Copying and derivations permitted under the MIT license, see LICENSE.txt.
