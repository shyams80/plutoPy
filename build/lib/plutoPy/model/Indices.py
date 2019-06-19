"""Indices

sources: https://nseindia.com/ https://bseindia.com/

.. module:: Indices
    :synopsis: Query index time-series from various sources
"""

from sqlalchemy import Column, Integer, String, Date, Float, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from datetime import date, datetime

from .Db import StockViz

Base = declarative_base()

class NseTimeSeries(Base, StockViz):
    """Query the index time-series published by the NSE"""
    
    __tablename__ = 'BHAV_INDEX'
    
    NAME = Column('INDEX_NAME', String(254), nullable=False) #: name of the index. Use this to query the time-series
    TIME_STAMP = Column(Date, nullable=False)
    
    HIGH = Column('PX_HIGH', Float, nullable=True)
    LOW = Column('PX_LOW', Float, nullable=True)
    OPEN = Column('PX_OPEN', Float, nullable=True)
    CLOSE = Column('PX_CLOSE', Float, nullable=True)

    VOLUME = Column('TRD_QTY', Float, nullable=True)
    
    __table_args__ = (PrimaryKeyConstraint('INDEX_NAME', 'TIME_STAMP'),)
    
    def __repr__(self):
        return f"{self.TIME_STAMP.strftime('%Y-%b-%d')},{self.CLOSE}"

class BseTimeSeries(Base, StockViz):
    """Query the index time-series published by the BSE"""
    
    __tablename__ = 'BHAV_INDEX_BSE'
    
    NAME = Column('INDEX_NAME', String(254), nullable=False)
    TIME_STAMP = Column(Date, nullable=False)
    
    HIGH = Column('PX_HIGH', Float, nullable=True)
    LOW = Column('PX_LOW', Float, nullable=True)
    OPEN = Column('PX_OPEN', Float, nullable=True)
    CLOSE = Column('PX_CLOSE', Float, nullable=True)

    __table_args__ = (PrimaryKeyConstraint('INDEX_NAME', 'TIME_STAMP'),)
    
    def __repr__(self):
        return f"{self.TIME_STAMP.strftime('%Y-%b-%d')},{self.CLOSE}"