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
    
class NseConstituents(Base, StockViz):
    """Query the latest constituents of NSE indices"""
    
    __tablename__ = 'INDEX_NSE_3'    
    
    NAME = Column('INDEX_NAME', String(50), nullable=False) #: name of the index. Use this to query the constituents
    TIME_STAMP = Column(Date, nullable=False) #: date when the constituents of the index was updated
    
    SYMBOL = Column(String(10), nullable=False)
    INDUSTRY = Column(String(50), nullable=False)
    CAP_WEIGHT = Column(Float, nullable=True)
    
    __table_args__ = (PrimaryKeyConstraint('INDEX_NAME', 'TIME_STAMP', 'SYMBOL'),)
    
    def __repr__(self):
        return f"{self.NAME}:  {self.SYMBOL}"

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
    
class BseConstituents(Base, StockViz):
    """Query the latest constituents of BSE indices"""
    
    __tablename__ = 'INDEX_BSE2'    
    
    NAME = Column('INDEX_NAME', String(50), nullable=False) #: name of the index. Use this to query the constituents
    TIME_STAMP = Column('INDEX_DATE', Date, nullable=False) #: date when the constituents of the index was updated
    
    CODE = Column('SECURITY_CODE', Integer, nullable=False) #: BSE security code
    SYMBOL = Column('NSE_SYMBOL', String(10), nullable=True) #: NSE symbol, if the security is listed in the NSE

    SECURITY_NAME = Column(String(254), nullable=False) #: name of the security
    
    __table_args__ = (PrimaryKeyConstraint('INDEX_NAME', 'INDEX_DATE', 'SECURITY_CODE'),)
    
    def __repr__(self):
        return f"{self.NAME}:  {self.SECURITY_NAME}"    