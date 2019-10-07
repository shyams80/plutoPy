"""Indices

sources: 
    https://nseindia.com/ 
    https://bseindia.com/ 
    https://www.ccilindia.com 
    https://finance.yahoo.com/
    https://indices.barclays
    https://wilshire.com/indexes

.. module:: Indices
    :synopsis: Query index time-series from various sources
"""

from sqlalchemy import Column, Integer, String, Date, Float, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from datetime import date, datetime

from .Db import StockViz, StockVizUs2

Base = declarative_base()

class IndiaVixTimeSeries(Base, StockViz):
    """Query the India VIX time-series data published by the NSE"""
    
    __tablename__ = 'VIX_HISTORY'
    
    TIME_STAMP = Column(Date, primary_key=True, nullable=False)
    
    HIGH = Column('PX_HIGH', Float, nullable=True)
    LOW = Column('PX_LOW', Float, nullable=True)
    OPEN = Column('PX_OPEN', Float, nullable=True)
    CLOSE = Column('PX_CLOSE', Float, nullable=True)
    
    def __repr__(self):
        return f"{self.TIME_STAMP.strftime('%Y-%b-%d')}: {self.CLOSE}"
    

class IndiaGsecTimeSeries(Base, StockViz):
    """Query the Indian Government Soverign Bond index time-series published by the CCIL"""
    
    __tablename__ = 'INDEX_CCIL_TENOR'
    
    NAME = Column('INDEX_NAME', String(254), nullable=False) #: tenor bucket. possible values: 0_5, 5_10, 10_15, 15_20, 20_30
    TIME_STAMP = Column(Date, nullable=False)
    
    TRI = Column(Float, nullable=True) #: Total Return Index. the absolute return that the tenor bucket offers. includes coupon accrued and capital gains (losses)
    PRI = Column(Float, nullable=True) #: Principal Return Index. based on clean price
    COUPON = Column(Float, nullable=True) #: wavg coupon
    YTM = Column(Float, nullable=True) #: wavg yield-to-maturity
    DURATION = Column(Float, nullable=True) #: wavg duration
    
    __table_args__ = (PrimaryKeyConstraint('INDEX_NAME', 'TIME_STAMP'),)
    
    def __repr__(self):
        return f"{self.TIME_STAMP.strftime('%Y-%b-%d')},{self.NAME}: {self.TRI}, {self.YTM}, {self.DURATION}"
    

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
        return f"{self.TIME_STAMP.strftime('%Y-%b-%d')}: {self.NAME},{self.CLOSE}"
    

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
        return f"{self.NAME}: {self.SYMBOL}"


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
        return f"{self.NAME}: {self.SECURITY_NAME}"   
    
class YahooFinanceTimeSeries(Base, StockVizUs2):
    """Query the index time-series published by Yahoo Finance"""
    
    __tablename__ = 'BHAV_YAHOO'
    
    NAME = Column('SYMBOL', String(50), nullable=False) #: name of the index. Use this to query the time-series
    TIME_STAMP = Column(Date, nullable=False)
    
    HIGH = Column('H', Float, nullable=True)
    LOW = Column('L', Float, nullable=True)
    OPEN = Column('O', Float, nullable=True)
    CLOSE = Column('C', Float, nullable=True)
    CLOSE_ADJ = Column('AC', Float, nullable=True)

    VOLUME = Column('V', Float, nullable=True)
    
    __table_args__ = (PrimaryKeyConstraint('SYMBOL', 'TIME_STAMP'),)
    
    def __repr__(self):
        return f"{self.TIME_STAMP.strftime('%Y-%b-%d')}: {self.NAME}, {self.CLOSE}"
    
class BarclaysMeta(Base, StockVizUs2):
    """Meta information about the BarclaysTimeSeries by TICKER"""
    
    __tablename__ = 'BARCLAYS_META'
    
    TICKER = Column(String(50), primary_key=True, nullable=False)
    DATE_LIVE = Column(Date, nullable=True) #: Date when the index went live
    DATE_BASE = Column(Date, nullable=True) #: Date from when the index is calculated
    
    NAME = Column('NAME_WEB', String(126), nullable=True)
    FAMILY = Column('NAME_FAMILY', String(50), nullable=True)
    
    RETURN_TYPE = Column(String(50), nullable=True) #: Excess/Price/Total Return
    CURRENCY = Column(String(10), nullable=True)
    
    def __repr__(self):
        return f"{self.TICKER}: {self.FAMILY}/{self.NAME}/{self.RETURN_TYPE}, {self.CURRENCY}"

class BarclaysTimeSeries(Base, StockVizUs2):
    """Query the index time-series published by Barclays"""
    
    __tablename__ = 'BARCLAYS_DATA'
    
    TICKER = Column(String(50), nullable=False)
    TIME_STAMP = Column(Date, nullable=False)
    CLOSE = Column('VAL', Float, nullable=False)
    
    __table_args__ = (PrimaryKeyConstraint('TICKER', 'TIME_STAMP'),)
    
    def __repr__(self):
        return f"{self.TIME_STAMP.strftime('%Y-%b-%d')}: {self.TICKER}, {self.CLOSE}"

class WilshireMeta(Base, StockVizUs2):
    """Grab the ID to access the time-series"""
    
    __tablename__ = 'WILSHIRE_INDEX_META'
    
    ID = Column(Integer, primary_key=True, nullable=False)
    NAME = Column('INDEX_NAME', String(126), nullable=False)
    
    def __repr__(self):
        return f"{self.ID}: {self.NAME}"


class WilshireTimeSeries(Base, StockVizUs2):
    """Query the index time-series published by Wilshire"""
    
    __tablename__ = 'WILSHIRE_INDEX_DATA'
    
    ID = Column(Integer, nullable=False)
    TIME_STAMP = Column(Date, nullable=False)
    CLOSE = Column('TR', Float, nullable=False)
    
    __table_args__ = (PrimaryKeyConstraint('ID', 'TIME_STAMP'),)
    
    def __repr__(self):
        return f"{self.TIME_STAMP.strftime('%Y-%b-%d')}: {self.ID}, {self.CLOSE}"
    