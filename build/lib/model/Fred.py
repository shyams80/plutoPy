"""St. Louis Fed FRED cache

sources: https://fred.stlouisfed.org/

.. module:: Fred
    :synopsis: Query the St. Louis Fed FRED database cache
"""
from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import date, datetime

from .Db import StockVizUs

Base = declarative_base()

class TimeSeries(Base, StockVizUs):
    """Query the FRED time-series cache"""
    
    __tablename__ = 'FRED_OBSERVATION'
    
    SERIES_ID = Column(Integer, primary_key=True, nullable=False)
    TIME_STAMP = Column(Date, nullable=False)
    VAL = Column(Float, nullable=False)
    
    def __repr__(self):
        return f"{self.TIME_STAMP.strftime('%Y-%b-%d')},{self.VAL}"
    
class Meta(Base, StockVizUs):
    """Query the FRED meta-data cache"""
    
    __tablename__ = 'FRED_SERIES'
    
    SERIES_ID = Column('ID', Integer, primary_key=True, nullable=False) #: use this to query the time-series
    TICKER = Column('SERIES_ID', String(126), nullable=False) #: FRED id
    NAME = Column('TITLE', String(510)) #: title
    FREQUENCY = Column('FREQ', String(10)) #: 'D' for day, 'M' for month, 'Q' for quarter, etc.
    UNITS = Column(String(510)) #: 'Miles', 'Million of Dollars', etc.
    SEASON_ADJUST = Column(String(5)) #: 'SA' for seasonally adjusted, etc.   
    
    def __repr__(self):
        return f"{self.TICKER}: {self.NAME}"