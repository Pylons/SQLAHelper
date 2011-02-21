import os
import shutil
import tempfile
import unittest

import sqlalchemy as sa
from sqlalchemy.engine.base import Engine

import pyramid_sqla as psqla

class DBInfo(object):
    def __init__(self, dir, filename):
        self.file = os.path.join(dir, filename)
        self.url = "sqlite:///" + self.file

class PyramidSQLATestCase(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.db1 = DBInfo(self.dir, "db1.sqlite")
        self.db2 = DBInfo(self.dir, "db2.sqlite")
        self.db3 = DBInfo(self.dir, "db3.sqlite")

    def tearDown(self):
        psqla.reset()
        shutil.rmtree(self.dir, True)

    if not hasattr(unittest.TestCase, "assertIsInstance"): # pragma: no cover
        def assertIsInstance(self, obj, classes):
            if not isinstance(obj, classes):
                typ = type(obj)
                if isinstance(classes, (list, tuple)):
                    classes_str = ", ".join(x.__name__ for x in classes)
                    classes_str = "[%s]" % classes_str
                else:
                    classes_str = classes.__name__
                msg = "%s is not an instance of %s" % (typ, classes_str)
                raise AssertionError(msg)

        def assertIs(self, a, b):
            if a is not b:
                raise AssertionError("%r is not %r" % (a, b))


class TestAddEngine(PyramidSQLATestCase):
    def test_keyword_args(self):
        engine = psqla.add_engine(url=self.db1.url)
        self.assertIsInstance(engine, Engine)

    def test_simplest_settings(self):
        settings = {"sqlalchemy.url": self.db1.url}
        engine = psqla.add_engine(settings, prefix="sqlalchemy.")
        self.assertIsInstance(engine, Engine)

    def test_existing_engine(self):
        e = sa.create_engine(self.db1.url)
        engine = psqla.add_engine(engine=e)
        self.assertIs(engine, e)

    def test_multiple_engines(self):
        settings = {
            "sqlalchemy.url": self.db1.url,
            "stats.url": self.db2.url,
            "foo": "bar"}
        default = psqla.add_engine(settings)
        stats = psqla.add_engine(settings, name="stats", prefix="stats.")
        # Can we retrieve the engines?
        self.assertIs(psqla.get_engine(), default)
        self.assertIs(psqla.get_engine("default"), default)
        self.assertIs(psqla.get_engine("stats"), stats)
        # Are the session binding and base binding set correctly?
        self.assertIs(psqla.get_session().bind, default)
        self.assertIs(psqla.get_base().metadata.bind, default)

    def test_multiple_engines_without_default(self):
        settings = {
            "db1.url": self.db1.url,
            "db2.url": self.db2.url,
            "foo": "bar"}
        db1 = psqla.add_engine(settings, name="db1", prefix="db1.")
        db2 = psqla.add_engine(settings, name="db2", prefix="db2.")
        # Can we retrieve the engines?
        self.assertIs(psqla.get_engine("db1"), db1)
        self.assertIs(psqla.get_engine("db2"), db2)
        # There should be no default engine
        self.assertIs(psqla.get_session().bind, None)
        self.assertIs(psqla.get_base().metadata.bind, None)
        self.assertRaises(RuntimeError, psqla.get_engine)

class TestDeclarativeBase(PyramidSQLATestCase):
    def test1(self):
        import transaction
        Base = psqla.get_base()
        class Person(Base):
            __tablename__ = "people"
            id = sa.Column(sa.Integer, primary_key=True)
            first_name = sa.Column(sa.Unicode(100), nullable=False)
            last_name = sa.Column(sa.Unicode(100), nullable=False)
        psqla.add_engine(url=self.db1.url)
        Base.metadata.create_all()
        fred = Person(id=1, first_name=u"Fred", last_name=u"Flintstone")
        wilma = Person(id=2, first_name=u"Wilma", last_name=u"Flintstone")
        barney = Person(id=3, first_name=u"Barney", last_name=u"Rubble")
        betty = Person(id=4, first_name=u"Betty", last_name=u"Rubble")
        Session = psqla.get_session()
        sess = Session()
        sess.add_all([fred, wilma, barney, betty])
        transaction.commit()
        sess.expunge_all()
        del fred, wilma, barney, betty
        # Can we get back a record?
        barney2 = sess.query(Person).get(3)
        self.assertEqual(barney2.id, 3)
        self.assertEqual(barney2.first_name, u"Barney")
        self.assertEqual(barney2.last_name, u"Rubble")
        sa.select([Person.first_name])
        # Can we iterate the first names in reverse alphabetical order?
        q = sess.query(Person.first_name).order_by(Person.first_name.desc())
        result = [x.first_name for x in q]
        control = [u"Wilma", u"Fred", u"Betty", u"Barney"]
        self.assertEqual(result, control)

    def test1_without_transaction_manager(self):
        Base = psqla.get_base()
        class Person(Base):
            __tablename__ = "people"
            id = sa.Column(sa.Integer, primary_key=True)
            first_name = sa.Column(sa.Unicode(100), nullable=False)
            last_name = sa.Column(sa.Unicode(100), nullable=False)
        psqla.add_engine(url=self.db1.url)
        Base.metadata.create_all()
        fred = Person(id=1, first_name=u"Fred", last_name=u"Flintstone")
        wilma = Person(id=2, first_name=u"Wilma", last_name=u"Flintstone")
        barney = Person(id=3, first_name=u"Barney", last_name=u"Rubble")
        betty = Person(id=4, first_name=u"Betty", last_name=u"Rubble")
        Session = psqla.get_session()
        Session.configure(extension=None)  # XXX Kludge for SQLAlchemy/ZopeTransactionExtension bug
        sess = Session()
        sess.add_all([fred, wilma, barney, betty])
        sess.commit()
        sess.expunge_all()
        del fred, wilma, barney, betty
        # Can we get back a record?
        barney2 = sess.query(Person).get(3)
        self.assertEqual(barney2.id, 3)
        self.assertEqual(barney2.first_name, u"Barney")
        self.assertEqual(barney2.last_name, u"Rubble")
        sa.select([Person.first_name])
        # Can we iterate the first names in reverse alphabetical order?
        q = sess.query(Person.first_name).order_by(Person.first_name.desc())
        result = [x.first_name for x in q]
        control = [u"Wilma", u"Fred", u"Betty", u"Barney"]
        self.assertEqual(result, control)

class Test_add_engine(unittest.TestCase):
    def setUp(self):
        self.engines = {}
        self.session = DummySession()
        self.base = DummyBase()
        self.old_engines = psqla._engines
        self.old_base = psqla._base
        self.old_session = psqla._session
        psqla._engines = self.engines
        psqla._base = self.base
        psqla._session = self.session

    def tearDown(self):
        psqla._engines = self.old_engines
        psqla._base = self.old_base
        psqla._session = self.old_session

    def _callFUT(self, settings=None, name='default', prefix='sqlalchemy.',
                 engine=None, **engine_args):
        return psqla.add_engine(
            settings=settings, name=name, prefix=prefix, engine=engine,
            **engine_args)

    def test_both_engine_and_settings(self):
        self.assertRaises(TypeError, self._callFUT, engine=True, settings=True)

    def test_both_engine_and_engine_args(self):
        self.assertRaises(TypeError, self._callFUT, engine=True, foo='bar')

    def test_explicit_engine(self):
        engine = DummyEngine()
        e = self._callFUT(engine=engine)
        self.failUnless(e is engine)
        self.failUnless(self.engines['default'], None)
        self.assertEqual(self.session.bind, e)
        self.assertEqual(self.base.metadata.bind, e)

    def test_engine_from_settings_no_prefix(self):
        self.assertRaises(
            ValueError,
            self._callFUT, prefix='',
            settings={'sqlalchemy.url':'sqlite:///:memory:'})

    def test_engine_from_settings_no_url(self):
        self.assertRaises(ValueError, self._callFUT, settings={'a':'1'})

    def test_engine_from_settings_no_url_bad_prefix(self):
        self.assertRaises(ValueError,
                          self._callFUT, prefix='fudge', settings={'a':'1'})

    def test_url_from_engine_args(self):
        from sqlalchemy.engine.base import Engine
        e = self._callFUT(url='sqlite:///:memory:')
        self.assertEqual(e.__class__, Engine)

    def test_url_from_engine_args_no_url(self):
        self.assertRaises(TypeError, self._callFUT, settings=None)

    def test_engine_from_settings(self):
        from sqlalchemy.engine.base import Engine
        e = self._callFUT(settings={'sqlalchemy.url':'sqlite:///:memory:'})
        self.assertEqual(e.__class__, Engine)

class DummySession(object):
    def configure(self, **kw):
        self.__dict__.update(kw)

class DummyMetadata(object):
    pass

class DummyBase(object):
    def __init__(self):
        self.metadata = DummyMetadata()

class DummyEngine(object):
    pass
