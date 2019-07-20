"""Commodity Futures and Options

sources: https://www.mcxindia.com/ https://www.ncdex.com/ https://www.cmegroup.com/

.. module:: CommodityFuturesAndOptions
    :synopsis: Query information about commodity futures and options listed in various exchanges 
"""

from sqlalchemy import Column, Integer, BigInteger, String, Date, Float, Boolean, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from datetime import date, datetime

from .Db import StockViz

Base = declarative_base()

class CmeEod(Base, StockViz):
    """Query the end-of-day prices of commodity futures contracts traded on the COMEX and NYMEX"""
    
    __tablename__ = 'CME_BHAV'
    
    CONTRACT = Column(String(10), nullable=False)
    TIME_STAMP = Column(Date, nullable=True)
    
    PRODUCT_SYMBOL = Column(String(10), nullable=False)
    PRODUCT_DESCRIPTION = Column(String(254), nullable=False)
    
    CONTRACT_MONTH = Column(Integer, nullable=False)
    CONTRACT_YEAR = Column(Integer, nullable=False)
    CONTRACT_DAY = Column(Integer, nullable=False)
    
    HIGH = Column('PX_HIGH', Float, nullable=True)
    LOW = Column('PX_LOW', Float, nullable=True)
    OPEN = Column('PX_OPEN', Float, nullable=True)
    LAST = Column('PX_LAST', Float, nullable=True)
    SETTLE = Column(Float, nullable=True)
    
    VOLUME = Column(Float, nullable=True)
    
    __table_args__ = (PrimaryKeyConstraint('CONTRACT', 'TIME_STAMP'),)
    
    def __repr__(self):
        return f"{self.TIME_STAMP.strftime('%Y-%b-%d')}/{self.CONTRACT}: {self.LAST},{self.SETTLE},{self.VOLUME}"
    
    
class McxEod(Base, StockViz):
    """Query the end-of-day prices of commodity contracts traded on the MCX"""
    
    __tablename__ = 'BHAV_COM_MCX'
    
    CONTRACT = Column(String(50), nullable=False)
    TIME_STAMP = Column(Date, nullable=True)
    
    EXPIRY = Column(Date, nullable=True)
    EXPIRY_SERIES = Column(Integer, nullable=True) #: 0 implies current month contract, etc.
    
    OTYPE = Column(String(50), nullable=False) #: CE - European calls; PE - European puts; XX , FUTCOM - futures
    STRIKE = Column(Float, nullable=False) #: if OTYPE is CE or PE, then the strike
    
    HIGH = Column('PX_HIGH', Float, nullable=True)
    LOW = Column('PX_LOW', Float, nullable=True)
    OPEN = Column('PX_OPEN', Float, nullable=True)
    CLOSE = Column('PX_CLOSE', Float, nullable=True)
    
    VOLUME = Column(Float, nullable=False) #: number of contracts traded
    VOL = Column(Float, nullable=False) #: quantity of the underlying commodity traded in VOL_UNITS
    VOL_UNITS = Column(String(10), nullable=False) #: BALES, KGS, BBL, etc...
    
    VALUE = Column(Float, nullable=False) #: value of the contracts traded
    OI = Column(Float, nullable=False) #: open interest
    
    __table_args__ = (PrimaryKeyConstraint('CONTRACT', 'TIME_STAMP', 'EXPIRY', 'OTYPE', 'STRIKE'),)
    
    def __repr__(self):
        return f"{self.TIME_STAMP.strftime('%Y-%b-%d')}/{self.CONTRACT}/{self.EXPIRY.strftime('%Y-%b-%d')}/{self.OTYPE}/{self.STRIKE}: {self.CLOSE},{self.VOLUME}"
    

class NcdexEod(Base, StockViz):
    """Query the end-of-day prices of commodity contracts traded on the NCDEX"""
    
    __tablename__ = 'BHAV_COM_NCDEX'
    
    CONTRACT = Column('SYMBOL', String(50), nullable=False)
    TIME_STAMP = Column(Date, nullable=True)
    
    EXPIRY = Column(Date, nullable=True)
    EXPIRY_SERIES = Column(Integer, nullable=True) #: 0 implies current month contract, etc.
    
    COMMODITY = Column(String(254), nullable=False) #: Crude palm oil, TURMERIC, etc...
    DELIVERY_CENTRE = Column(String(254), nullable=False) #: Ahmedabad, Kandla, etc...
    
    HIGH = Column('H', Float, nullable=True)
    LOW = Column('L', Float, nullable=True)
    OPEN = Column('O', Float, nullable=True)
    CLOSE = Column('C', Float, nullable=True)
    
    PRICE_UNIT = Column(String(62), nullable=False) #: RS/QUINTAL, RS/10KGS, RS/BALES, etc...
    
    TRADED_QTY = Column(Integer, nullable=True) #: number of contracts traded
    MEASURE = Column(String(14), nullable=True) #: for VOLUME. MT, LOT, etc
    
    TRADED_NUM = Column(Integer, nullable=True) #: number of trades
    TRADED_VAL = Column('TRADED_VAL_LAKHS', Float, nullable=True) #: traded value in Rs. lakhs
    
    OI = Column(Float, nullable=False) #: open interest
    LAST_TRADE = Column('LAST_TRADE_DT', Date, nullable=True) #: day on which the last trade occurred
    
    __table_args__ = (PrimaryKeyConstraint('SYMBOL', 'TIME_STAMP', 'EXPIRY'),)
    
    def __repr__(self):
        return f"{self.TIME_STAMP.strftime('%Y-%b-%d')}/{self.CONTRACT}/{self.EXPIRY.strftime('%Y-%b-%d')}: {self.CLOSE},{self.TRADED_QTY}"
    
        