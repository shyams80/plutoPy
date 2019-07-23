"""Currencies

sources: https://www.alphavantage.co https://www.nseindia.com/ 

.. module:: Currencies
    :synopsis: Query information about currency futures and options from various sources
"""

from sqlalchemy import Column, Integer, BigInteger, String, Date, DateTime, Float, Boolean, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from datetime import date, datetime

from .Db import StockViz, StockVizBeka

Base = declarative_base()

class NseFuturesTimeSeries(Base, StockViz):
    """Query the currency futures time-series published by the NSE"""
    
    __tablename__ = 'BHAV_CUR_FUT'
    
    TIME_STAMP = Column(Date, nullable = False)
    
    SYMBOL = Column(String(10), nullable=False) 
    EXPIRY = Column('EXPIRY_DT', Date, nullable=False) 
    
    HIGH = Column('PX_HIGH', Float, nullable=True)
    LOW = Column('PX_LOW', Float, nullable=True)
    OPEN = Column('PX_OPEN', Float, nullable=True)
    CLOSE = Column('PX_CLOSE', Float, nullable=True)
    SETTLE = Column('PX_SETTLE', Float, nullable=True)
    
    CONTRACTS = Column('TRADED_CONTRACTS', Integer, nullable=True) 
    VALUE = Column('TRADED_VAL', Float, nullable=True) 
    OI = Column('OI_CONTRACTS', Integer, nullable=True) 
    
    __table_args__ = (PrimaryKeyConstraint('SYMBOL', 'EXPIRY_DT', 'TIME_STAMP'),)
    
    def __repr__(self):
        return f"{self.SYMBOL}({self.EXPIRY.strftime('%Y-%b-%d')})/{self.TIME_STAMP.strftime('%Y-%b-%d')}: {self.HIGH},{self.LOW},{self.OPEN},{self.CLOSE},{self.VALUE},{self.OI}"
    
class NseOptionsTimeSeries(Base, StockViz):
    """Query the currency option time-series published by the NSE"""
    
    __tablename__ = 'BHAV_CUR_OPT'
    
    TIME_STAMP = Column(Date, nullable = False)
    
    SYMBOL = Column(String(10), nullable=False) 
    EXPIRY = Column(Date, nullable=False) 
    STRIKE = Column(Float, nullable=False)
    OTYPE = Column('OPTION_TYPE', String(5), nullable=False) 
    
    HIGH = Column('PX_HIGH', Float, nullable=True)
    LOW = Column('PX_LOW', Float, nullable=True)
    OPEN = Column('PX_OPEN', Float, nullable=True)
    CLOSE = Column('PX_CLOSE', Float, nullable=True) 
    SETTLE = Column('PX_SETTLE', Float, nullable=True)
    
    CONTRACTS = Column('TRATED_CONTRACTS', Integer, nullable=True) 
    VALUE = Column('NOTIONAL_VALUE', Float, nullable=True) 
    OI = Column('OI_CONTRACTS', Integer, nullable=True) 
    
    __table_args__ = (PrimaryKeyConstraint('SYMBOL', 'EXPIRY', 'TIME_STAMP', 'STRIKE', 'OPTION_TYPE'),)
    
    def __repr__(self):
        return f"{self.SYMBOL}({self.EXPIRY.strftime('%Y-%b-%d')})/{self.STRIKE}{self.OTYPE}/{self.TIME_STAMP.strftime('%Y-%b-%d')}: {self.HIGH},{self.LOW},{self.OPEN},{self.CLOSE},{self.VALUE},{self.OI}" 
    
class AvEodTimeSeries(Base, StockVizBeka):
    """Query the end-of-day currency USD-fx time-series published by AlphaVantage"""
    
    __tablename__ = 'av_fx_usd_daily_ts'
    
    TIME_STAMP = Column('time_stamp', Date, nullable = False) #: in UTC
    SYMBOL = Column('curr_code', String(5), nullable=False) 
    
    HIGH = Column('px_high', Float, nullable=True)
    LOW = Column('px_low', Float, nullable=True)
    OPEN = Column('px_open', Float, nullable=True)
    CLOSE = Column('px_close', Float, nullable=True)
    
    __table_args__ = (PrimaryKeyConstraint('curr_code', 'time_stamp'),)
    
    def __repr__(self):
        return f"{self.SYMBOL}/{self.TIME_STAMP.strftime('%Y-%b-%d')}: {self.HIGH},{self.LOW},{self.OPEN},{self.CLOSE}"
    
class Av30minTimeSeries(Base, StockVizBeka):
    """Query the 30-min bar of currency USD-fx time-series published by AlphaVantage"""
    
    __tablename__ = 'av_fx_usd_30min_ts'
    
    TIME_STAMP = Column('time_stamp', DateTime, nullable = False) #: in UTC
    SYMBOL = Column('curr_code', String(5), nullable=False) 
    
    HIGH = Column('px_high', Float, nullable=True)
    LOW = Column('px_low', Float, nullable=True)
    OPEN = Column('px_open', Float, nullable=True)
    CLOSE = Column('px_close', Float, nullable=True)
    
    __table_args__ = (PrimaryKeyConstraint('curr_code', 'time_stamp'),)
    
    def __repr__(self):
        return f"{self.SYMBOL}/{self.TIME_STAMP.strftime('%Y-%b-%d')}: {self.HIGH},{self.LOW},{self.OPEN},{self.CLOSE}"    
    
    