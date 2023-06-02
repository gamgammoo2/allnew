from sqlalchemy import Column, TEXT, INT,LargeBinary
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ufTotal(Base):
    __tablename__="uf_total"

    DATADATE1 = Column(TEXT, nullable=True, primary_key=True)
    COUNT1 = Column(INT,nullable=True)
    DATADATE2 = Column(TEXT, nullable=True)
    COUNT2 = Column(INT,nullable=True)

class ufGraph(Base):
    __tablename__="graphdb"

    fire = Column(LargeBinary, nullable=False, primary_key=True)
    uf = Column(LargeBinary,nullable=False) 
    temppredict = Column(LargeBinary,nullable=False) 

class fireTotal(Base):
    __tablename__="fire_total"

    DATADATE1 = Column(TEXT, nullable=True, primary_key=True)
    COUNT1 = Column(INT,nullable=True)
    DATADATE2 = Column(TEXT, nullable=True)
    COUNT2 = Column(INT,nullable=True)