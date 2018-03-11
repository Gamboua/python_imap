from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Date

engine = create_engine('sqlite:///dev.db')

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

Base = declarative_base()

class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer,primary_key=True)
    date = Column(Date)
    origin = Column(String)
    subject = Column(String)


if __name__ == '__main__':
  Base.metadata.create_all(engine)
