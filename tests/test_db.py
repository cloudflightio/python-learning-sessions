from uuid import uuid4

import pytest
import sqlalchemy

from learning_group.database import Book, Database, User
from testcontainers.postgres import PostgresContainer


@pytest.fixture
def db_engine():
    with PostgresContainer("postgres:13") as postgres:
        engine = sqlalchemy.create_engine(postgres.get_connection_url())
        (version,) = engine.execute("select version()").fetchone()
        print(version)  # 5.7.17
        yield engine


def test_abc(db_engine):
    db_engine.execute("create table a (x integer, y integer);")
    db_engine.execute("INSERT INTO a (x, y) VALUES (1, 2);")
    value = db_engine.execute("select y from a limit 1;").fetchone()
    assert value[0] == 2


def fill_with_test_data(db):
    with db.session_factory.begin() as session:
        tolkien = User(name="Tolkien")
        session.add(tolkien)
        session.add_all(
            [
                Book(title="The Fellowship of the Ring", author=tolkien),
                Book(title="The Two Towers", author=tolkien),
                Book(title="The Return of the King", author=tolkien),
            ]
        )
        king = User(name="Stephen King")
        session.add_all(
            [
                Book(title="The Gunslinger", author=king),
                Book(title="The Drawing of the Three", author=king),
                Book(title="The Waste Lands", author=king),
                Book(title="Wizard and Glass", author=king),
            ]
        )


def test_tables(db_engine):
    db = Database(db_engine)
    fill_with_test_data(db)

    with db.session_factory.begin() as session:
        assert session.query(User).count() == 2


def test_empty_tables(db_engine):
    db = Database(db_engine)
    with db.session_factory.begin() as session:
        assert session.query(Book).count() == 0
