from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


engine = create_engine(
    'mysql://transaction:osmentos@mysqltransdb:3306/transaction', echo=True)

Base = declarative_base()


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    _to = Column(Integer)
    _from = Column(Integer)
    record_id = Column(Integer, unique=True)
    amount = Column(Integer)


Transaction.__table__.create(bind=engine, checkfirst=True)


class Wallet(Base):
    __tablename__ = 'wallet'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    balance = Column(Integer)


Wallet.__table__.create(bind=engine, checkfirst=True)
