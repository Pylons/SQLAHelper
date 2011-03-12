SQLAHeler is a small library for SQLAlchemy web applications. It was written
for Pyramid but is not framework-specific. It acts as a container for the
application's contextual session, engines, and declarative base. This avoids
circular dependencies or the need for a 'meta' module if your model is split
across multiple modules.

The contextual session is initialized with the ZopeTransactionExtension so that
it can be used with transaction managers. This can be disabled if desired.

Version 1.0b1 is a public beta test before the final release.

It's currently tested on Python 2.6/Linux but should work on 2.5 and other
platforms. A set of unit tests is included.

Documentation is in the 'docs' directory.

(c) 2010-2011 Mike Orr
Copying and derivations permitted under the MIT license, see LICENSE.txt.
