"""Yale/Shiller Data-sets

source: http://www.econ.yale.edu/~shiller/data.htm

.. module:: Yale
    :synopsis: Query Yale/Shiller time-series
"""

from sqlalchemy import Column, Integer, String, Date, Float, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from datetime import date, datetime

from .Db import StockVizUs2

Base = declarative_base()

class Confidence(Base, StockVizUs2):
    """Query Stock Market Confidence Indexes produced by the Yale School of Management. (https://svz.bz/2NzetU3)"""
    
    __tablename__ = "YALE_CONFIDENCE"
    
    NAME = Column('INDEX_NAME', String(50), nullable=False)
    TIME_STAMP = Column(Date, nullable=False)
    
    VALUE = Column('VAL', Float, nullable=False)
    STD_ERR = Column(Float, nullable=True)
    
    __table_args__ = (PrimaryKeyConstraint('INDEX_NAME', 'TIME_STAMP'),)
    
    def __repr__(self):
        return f"{self.TIME_STAMP.strftime('%Y-%b-%d')},{self.NAME}: {self.VALUE}"
    
class SP500(Base, StockVizUs2):
    """Query the monthly stock price, dividends, and earnings data and the consumer price index."""   
    
    __tablename__ = "YALE_SPCOMP" 
    
    TIME_STAMP = Column(Date, primary_key=True, nullable=False)
    
    CLOSE = Column('VAL', Float, nullable=False)
    CLOSE_REAL = Column('VAL_REAL', Float, nullable=True)
    
    DIVIDEND = Column(Float, nullable=True)
    DIVIDEND_REAL = Column(Float, nullable=True)
    
    EARNINGS = Column(Float, nullable=True)
    EARNINGS_REAL = Column(Float, nullable=True)
    
    CPI = Column(Float, nullable=True)
    LONG_IR = Column(Float, nullable=True)
    
    CAPE = Column(Float, nullable=True)
    
    def __repr__(self):
        return f"{self.TIME_STAMP.strftime('%Y-%b-%d')}: {self.CLOSE}, {self.CAPE}"
    
