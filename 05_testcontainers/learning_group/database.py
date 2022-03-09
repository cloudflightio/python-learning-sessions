import uuid

from sqlalchemy import Column, ForeignKey, Index, Integer, String, func
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship, sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    author_of = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "documents"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="author_of")


class Database:
    def __init__(self, engine) -> None:
        self.engine = engine
        self.session_factory = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)
