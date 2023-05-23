from sqlalchemy import Column, TEXT, INT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ufTotal(Base):
    __tablename__="uf_total"

    DATADATE = Column(TEXT, nullable=False, primary_key=True)
    COUNT = Column(INT,nullable=False)
    
class ufHalf(Base):
    __tablename__="uf_half"

    DATADATE = Column(TEXT, nullable=False, primary_key=True)
    COUNT = Column(INT,nullable=False) 