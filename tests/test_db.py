import sqlalchemy
from testcontainers.postgres import PostgresContainer
import pytest


@pytest.fixture
def db():
    with PostgresContainer('postgres:13') as postgres:
        engine = sqlalchemy.create_engine(postgres.get_connection_url())
        version, = engine.execute("select version()").fetchone()
        print(version)  # 5.7.17
        yield engine


def test_abc(db):
    db.execute("create table a (x integer, y integer);")
    db.execute("INSERT INTO a (x, y) VALUES (1, 2);")
    value = db.execute("select y from a limit 1;").fetchone()
    assert value[0] == 2
