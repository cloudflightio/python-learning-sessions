import pytest
import sqlalchemy
from sqlalchemy import desc, func

from learning_group.database import Base, Book, Database, User
from testcontainers.postgres import PostgresContainer


@pytest.fixture(scope="session")
def db_engine():
    with PostgresContainer("postgres:13") as postgres:
        engine = sqlalchemy.create_engine(postgres.get_connection_url())
        (version,) = engine.execute("select version()").fetchone()
        print(version)

        # remove all tables and data
        Base.metadata.drop_all(engine)

        yield engine


@pytest.fixture
def empty_db_engine(db_engine):
    # remove all tables and data
    Base.metadata.drop_all(db_engine)

    yield db_engine


def test_abc(empty_db_engine):
    engine = empty_db_engine
    engine.execute("create table a (x integer, y integer);")
    engine.execute("INSERT INTO a (x, y) VALUES (1, 2);")
    value = engine.execute("select y from a limit 1;").fetchone()
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


def test_tables(empty_db_engine):
    db = Database(empty_db_engine)
    fill_with_test_data(db)

    with db.session_factory.begin() as session:
        assert session.query(User).count() == 2
        count_books_by_author = (
            session.query(User.name, func.count().label("book_count"))
            .join(Book)
            .group_by(User.name)
            .order_by(desc("book_count"))
            .all()
        )
        assert count_books_by_author == [("Stephen King", 4), ("Tolkien", 3)]


def test_empty_tables(empty_db_engine):
    db = Database(empty_db_engine)
    with db.session_factory.begin() as session:
        assert session.query(Book).count() == 0
