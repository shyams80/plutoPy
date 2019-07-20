"""Equities Futures and Options traded on the NSE

sources: https://www.nseindia.com/ 

.. module:: EquitiesFuturesAndOptionsIndiaNse
    :synopsis: Query information about equity futures and options listed on the National Stock Exchange (NSE) of India  
"""

from sqlalchemy import Column, Integer, BigInteger, String, Date, Float, Boolean, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from datetime import date, datetime

from .Db import StockViz

Base = declarative_base()

class FuturesEodTimeSeries(Base, StockViz):
    """Query the end-of-day prices of equity futures contracts traded on the NSE"""
    
    __tablename__ = 'BHAV_EQ_FUT'
    
    TIME_STAMP = Column(Date, nullable = False)
    
    SYMBOL = Column(String(10), nullable=False) 
    EXPIRY = Column('EXPIRY_DT', Date, nullable=False) 
    
    HIGH = Column('PX_HIGH', Float, nullable=True)
    LOW = Column('PX_LOW', Float, nullable=True)
    OPEN = Column('PX_OPEN', Float, nullable=True)
    CLOSE = Column('PX_CLOSE', Float, nullable=True) #: usually a weighted average of price x volume of the last 15-minutes of trading
    SETTLE = Column('PX_SETTLE', Float, nullable=True)
    
    CONTRACTS = Column(Integer, nullable=True) 
    VALUE = Column('VAL_IN_LAKH', Float, nullable=True) 
    OI = Column('OPEN_INTEREST',Integer, nullable=True) 
    
    __table_args__ = (PrimaryKeyConstraint('SYMBOL', 'EXPIRY_DT', 'TIME_STAMP'),)
    
    def __repr__(self):
        return f"{self.SYMBOL}({self.EXPIRY.strftime('%Y-%b-%d')})/{self.TIME_STAMP.strftime('%Y-%b-%d')}: {self.HIGH},{self.LOW},{self.OPEN},{self.CLOSE},{self.VALUE},{self.OI}"
    
class OptionsEodTimeSeries(Base, StockViz):
    """Query the end-of-day prices of equity options contracts traded on the NSE"""
    
    __tablename__ = 'BHAV_EQ_OPT'
    
    TIME_STAMP = Column(Date, nullable = False)
    
    SYMBOL = Column(String(10), nullable=False) 
    EXPIRY = Column('EXPIRY_DT', Date, nullable=False) 
    STRIKE = Column('STRIKE_PR', Float, nullable=False)
    OTYPE = Column('OPTION_TYP', String(5), nullable=False)  #: CE - European calls; CA - American calls, etc...
    
    HIGH = Column('PX_HIGH', Float, nullable=True)
    LOW = Column('PX_LOW', Float, nullable=True)
    OPEN = Column('PX_OPEN', Float, nullable=True)
    CLOSE = Column('PX_CLOSE', Float, nullable=True) #: usually a weighted average of price x volume of the last 15-minutes of trading
    SETTLE = Column('PX_SETTLE', Float, nullable=True)
    
    CONTRACTS = Column(Integer, nullable=True) 
    VALUE = Column('VAL_IN_LAKH', Float, nullable=True) 
    OI = Column('OPEN_INTEREST',Integer, nullable=True) 
    
    __table_args__ = (PrimaryKeyConstraint('SYMBOL', 'EXPIRY_DT', 'TIME_STAMP', 'STRIKE_PR', 'OPTION_TYP'),)
    
    def __repr__(self):
        return f"{self.SYMBOL}({self.EXPIRY.strftime('%Y-%b-%d')})/{self.STRIKE}{self.OTYPE}/{self.TIME_STAMP.strftime('%Y-%b-%d')}: {self.HIGH},{self.LOW},{self.OPEN},{self.CLOSE},{self.VALUE},{self.OI}" 
    
class OptionGreeks(Base, StockViz):
    """Query the end-of-day option greeks of equity options contracts traded on the NSE"""
    
    __tablename__ = 'EQ_OPTION_GREEKS'
    
    TIME_STAMP = Column(Date, nullable = False)
    
    SYMBOL = Column(String(10), nullable=False) 
    EXPIRY = Column('EXPIRY_DATE', Date, nullable=False) 
    STRIKE = Column(Float, nullable=False)
    OTYPE = Column('OPTION_TYPE', String(5), nullable=False)  #: CE - European calls; PE - European puts
    
    MODEL_PRICE = Column('MODEL_PX', Float, nullable=True)
    DELTA = Column(Float, nullable=True)
    THETA = Column(Float, nullable=True)
    VEGA = Column(Float, nullable=True)
    RHO = Column(Float, nullable=True)
    LAMBDA = Column(Float, nullable=True)
    GAMMA = Column(Float, nullable=True)
    IV = Column(Float, nullable=True)
    TTM = Column(Float, nullable=True) #: time to maturity measured in years
    RATE = Column(Float, nullable=True) #: the interest rate used in the calculation
    SIGMA = Column(Float, nullable=True) #: the volatility assumption used in the calculation
    
    __table_args__ = (PrimaryKeyConstraint('SYMBOL', 'EXPIRY_DATE', 'TIME_STAMP', 'STRIKE', 'OPTION_TYPE'),)
    
    def __repr__(self):
        return f"{self.SYMBOL}({self.EXPIRY.strftime('%Y-%b-%d')})/{self.STRIKE}{self.OTYPE}/{self.TIME_STAMP.strftime('%Y-%b-%d')}: {self.MODEL_PRICE},{self.DELTA},{self.THETA},{self.VEGA},{self.GAMMA},{self.IV}" 
    
    
class LotSize(Base, StockViz):
    """Query the lot-size of equity futures and options contracts traded on the NSE"""
    
    __tablename__ = 'MKT_LOT'
    
    SYMBOL = Column(String(10), nullable=False) 
    CONTRACT = Column(Date, nullable=False) #: expiry year and month. the 'date' part is always set to 1.
    LOT_SIZE = Column(Float, nullable=False)
    
    __table_args__ = (PrimaryKeyConstraint('SYMBOL', 'CONTRACT'),)
    
    def __repr__(self):
        return f"{self.SYMBOL}/{self.CONTRACT}: {self.LOT_SIZE}"
    
    
