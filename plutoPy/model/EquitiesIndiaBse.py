"""Equities India BSE

sources: https://bseindia.com/

.. module:: EquitiesIndiaBse
    :synopsis: Query information about equities listed in the Bombay Stock Exchange (BSE) of India 
"""

from sqlalchemy import Column, Integer, BigInteger, String, Date, Float, Boolean, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from datetime import date, datetime

from .Db import StockViz

Base = declarative_base()

class Tickers(Base, StockViz):
    """Query meta data of listed equity tickers"""
    
    __tablename__ = 'EQUITY_TICKER_BSE'
    
    ISIN = Column(String(12), primary_key=True, nullable=False) #: unique identifier
    CODE = Column('SC_CODE', BigInteger, nullable=False) #: BSE's unique identifier
    
    SYMBOL = Column('SC_ID', String(50), nullable=False) #: ticker/stock symbol. for eg: INFY
    SERIES = Column('SC_GROUP', String(5), nullable=False) #: A/B/T as assigned by the BSE
    
    NAME = Column('SC_NAME', String(254), nullable=False) #: name of the security. for eg: Infosys Limited
    
    FACE = Column('FACE_VALUE', Float, nullable = False) #: a stock's face value is the initial cost of the stock, as indicated on the certificate
    
    INDUSTRY = Column(String(254), nullable = False) #: BSE's industry classification
    
    def __repr__(self):
        return f"{self.SYMBOL}({self.SERIES}): {self.NAME}, {self.INDUSTRY}"
    
class MiscInfo(Base, StockViz):
    """Query miscellaneous information of listed equity tickers"""
    
    __tablename__ = 'EQUITY_MISC_INFO_BSE'
    
    CODE = Column('SC_CODE', BigInteger, nullable=False) #: BSE's unique identifier
    TIME_STAMP = Column(Date, nullable = False)
    
    FF_MKT_CAP_CR = Column(Float, nullable = True) #: free-float market-cap in crores
    FULL_MKT_CAP_CR = Column(Float, nullable = True) #: full-float market-cap in crores
    D2T_PCT = Column(Float, nullable = True) #: delivery percentage. % of shares which were not squared off the same day out of total shares traded
    
    __table_args__ = (PrimaryKeyConstraint('SC_CODE', 'TIME_STAMP'),)
    
    def __repr__(self):
        return f"{self.CODE}/{self.TIME_STAMP.strftime('%Y-%b-%d')}: {self.FF_MKT_CAP_CR},{self.FULL_MKT_CAP_CR},{self.D2T_PCT}"

class EodTimeSeries(Base, StockViz):
    """Query unadjusted end-of-day price and volume time-series for listed stocks"""
    
    __tablename__ = 'BSE_PX_HISTORY'
    
    CODE = Column('SC_CODE', BigInteger, nullable=False) #: BSE's unique identifier
    SERIES = Column('SC_GROUP', String(5), nullable=False) #: A/B/T as assigned by the BSE
    TIME_STAMP = Column(Date, nullable = False)
    
    NAME = Column('SC_NAME', String(254), nullable=False) #: name of the security. for eg: Infosys Limited
    TYPE = Column('SC_TYPE', String(5), nullable=False)
    
    HIGH = Column('PX_HIGH', Float, nullable=True)
    LOW = Column('PX_LOW', Float, nullable=True)
    OPEN = Column('PX_OPEN', Float, nullable=True)
    CLOSE = Column('PX_CLOSE', Float, nullable=True) #: usually a weighted average of price x volume of the last 15-minutes of trading
    LAST = Column('PX_LAST', Float, nullable=True) #: last traded price
    
    VOLUME = Column('NO_OF_SHRS', Float, nullable=True)
    NUM_TRADES = Column('NO_TRADES', Float, nullable=True)
    TURNOVER = Column('NET_TURNOV', Float, nullable=True) 
    
    __table_args__ = (PrimaryKeyConstraint('SC_CODE', 'SC_GROUP', 'TIME_STAMP'),)
    
    def __repr__(self):
        return f"{self.CODE}({self.SERIES})/{self.TIME_STAMP.strftime('%Y-%b-%d')}: {self.HIGH},{self.LOW},{self.OPEN},{self.CLOSE},{self.VOLUME}"

class CorporateResults(Base, StockViz):
    """Query to CorporateResults for a specific period and stock"""

    __tablename__ = 'CORP_RESULTS_KV_BSE'
    
    CODE = Column('SC_CODE', BigInteger, nullable=False) #: BSE's unique identifier
    PERIOD_BEGIN = Column(Date, nullable=False)
    PERIOD_END = Column(Date, nullable=False)
    IS_AUDITED = Column(Boolean, nullable=False)
    
    H1 = Column('HEADER', String(254), nullable=True) #: section 1
    
    KEY = Column('K', String(254), nullable=False)
    VALUE = Column('V', Float, nullable = False)
    
    AUTO_ID = Column(BigInteger, primary_key=True, nullable=False)
    
    def __repr__(self):
        return f"{self.PERIOD_BEGIN.strftime('%Y-%b-%d')}:{self.PERIOD_END.strftime('%Y-%b-%d')} {self.H1}/{self.KEY}: {self.VALUE}"