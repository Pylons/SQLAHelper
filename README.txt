SQLAHelper is a small library for SQLAlchemy web applications. It was written
for Pyramid but is not framework-specific. It acts as a container for the
application's contextual session, engines, and declarative base. This avoids
circular dependencies between the application's model modules, and allows
cooperating third-party libraries to use the session, base, and transaction.

The contextual session is initialized with the ZopeTransactionExtension so that
it can be used with transaction managers. This can be disabled if desired.

**SQLAHelper is under a maintenance freeze.**  If you would like to maintain
it, please bring it up on pylons-discuss. The repository has significant
updates beyond version 1, including a streamlined version 2 API, but no release
is scheduled.

Documentation is in the 'docs' directory.

(c) 2010-2012 Mike Orr and contributors
Copying and derivations permitted under the MIT license, see LICENSE.txt.
