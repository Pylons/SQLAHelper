import os
import shutil
import tempfile
import unittest

import sqlalchemy as sa
from sqlalchemy.engine.base import Engine
import sqlalchemy.ext.declarative as declarative

import sqlahelper

class DBInfo(object):
    def __init__(self, dir, filename):
        self.file = os.path.join(dir, filename)
        self.url = "sqlite:///" + self.file

class SQLAHelperTestCase(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.db1 = DBInfo(self.dir, "db1.sqlite")
        self.db2 = DBInfo(self.dir, "db2.sqlite")
        self.db3 = DBInfo(self.dir, "db3.sqlite")

    def tearDown(self):
        sqlahelper.reset()
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


class TestAddEngine(SQLAHelperTestCase):
    def test_one_engine(self):
        e = sa.create_engine(self.db1.url)
        sqlahelper.add_engine(e)
        retrieved = sqlahelper.get_engine()
        self.assertIs(retrieved, e)

    def test_multiple_engines(self):
        default = sa.create_engine(self.db1.url)
        stats = sa.create_engine(self.db2.url)
        sqlahelper.add_engine(default)
        sqlahelper.add_engine(stats, "stats")
        # Can we retrieve the engines?
        self.assertIs(sqlahelper.get_engine(), default)
        self.assertIs(sqlahelper.get_engine("default"), default)
        self.assertIs(sqlahelper.get_engine("stats"), stats)
        # Are the session binding and base binding set correctly?
        self.assertIs(sqlahelper.get_session().bind, default)
        self.assertIs(sqlahelper.get_base().metadata.bind, default)

    def test_multiple_engines_without_default(self):
        db1 = sa.create_engine(self.db1.url)
        db2 = sa.create_engine(self.db2.url)
        sqlahelper.add_engine(db1, "db1")
        sqlahelper.add_engine(db2, "db2")
        # Can we retrieve the engines?
        self.assertIs(sqlahelper.get_engine("db1"), db1)
        self.assertIs(sqlahelper.get_engine("db2"), db2)
        # There should be no default engine
        self.assertIsNone(sqlahelper.get_session().bind)
        self.assertIsNone(sqlahelper.get_base().metadata.bind)
        self.assertIsNone(sqlahelper.get_engine())


class TestDeclarativeBase(SQLAHelperTestCase):
    def test1(self):
        import transaction
        Base = sqlahelper.get_base()
        class Person(Base):
            __tablename__ = "people"
            id = sa.Column(sa.Integer, primary_key=True)
            first_name = sa.Column(sa.Unicode(100), nullable=False)
            last_name = sa.Column(sa.Unicode(100), nullable=False)
        engine = sa.create_engine(self.db1.url)
        sqlahelper.add_engine(engine)
        Base.metadata.create_all()
        fred = Person(id=1, first_name=u"Fred", last_name=u"Flintstone")
        wilma = Person(id=2, first_name=u"Wilma", last_name=u"Flintstone")
        barney = Person(id=3, first_name=u"Barney", last_name=u"Rubble")
        betty = Person(id=4, first_name=u"Betty", last_name=u"Rubble")
        Session = sqlahelper.get_session()
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
        Base = sqlahelper.get_base()
        class Person(Base):
            __tablename__ = "people"
            id = sa.Column(sa.Integer, primary_key=True)
            first_name = sa.Column(sa.Unicode(100), nullable=False)
            last_name = sa.Column(sa.Unicode(100), nullable=False)
        engine = sa.create_engine(self.db1.url)
        sqlahelper.add_engine(engine)
        Base.metadata.create_all()
        fred = Person(id=1, first_name=u"Fred", last_name=u"Flintstone")
        wilma = Person(id=2, first_name=u"Wilma", last_name=u"Flintstone")
        barney = Person(id=3, first_name=u"Barney", last_name=u"Rubble")
        betty = Person(id=4, first_name=u"Betty", last_name=u"Rubble")
        Session = sqlahelper.get_session()
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


class TestSetBase(SQLAHelperTestCase):
    def test1(self):
        base = sqlahelper.get_base()
        my_base = declarative.declarative_base()
        sqlahelper.set_base(my_base)
        base2 = sqlahelper.get_base()
        try:
            self.assertIsNot(base2, base)
            self.assertIs(base2, my_base)
        except AttributeError:  # Python < 2.7
            self.assertNotEqual(base2, base)
            self.assertEqual(base2, my_base)


if __name__ == "__main__":
    unittest.main()
