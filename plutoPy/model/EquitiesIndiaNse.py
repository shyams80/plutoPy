"""Equities India NSE

sources: https://nseindia.com/

.. module:: EquitiesIndiaNse
    :synopsis: Query information about equities listed in the National Stock Exchange (NSE) of India 
"""

from sqlalchemy import Column, Integer, BigInteger, String, Date, Float, Boolean, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from datetime import date, datetime

from .Db import StockViz, StockVizDyn
from .IntegerDate import IntegerDate

Base = declarative_base()

class Tickers(Base, StockViz):
    """Query meta data of listed equity tickers"""
    
    __tablename__ = 'EQUITY_TICKER'
    
    ISIN = Column(String(12), primary_key=True, nullable=False) #: unique identifier
    SYMBOL = Column(String(10), nullable=False) #: ticker/stock symbol. for eg: INFY
    SERIES = Column(String(5), nullable=False) #: EQ/BE/BZ as assigned by the NSE
    
    NAME = Column(String(510), nullable=False) #: name of the security. for eg: Infosys Limited
    
    DATE_LISTING = Column(Date, nullable = False) #: date of birth of the ticker
    
    PAID_UP = Column(Float, nullable = False) #: paid-up capital is the amount of money a company has received from shareholders in exchange for shares of stock
    FACE = Column(Float, nullable = False) #: a stock's face value is the initial cost of the stock, as indicated on the certificate
    
    MARKET_LOT = Column(Float, nullable = False) #: usually, you can trade just 1 stock. but sometimes, only in multiples of "market lot"
    
    def __repr__(self):
        return f"{self.SYMBOL}({self.SERIES}): {self.NAME}, {self.DATE_LISTING.strftime('%Y-%b-%d')}"
    
class MiscInfo(Base, StockViz):
    """Query miscellaneous information of listed equity tickers"""
    
    __tablename__ = 'EQUITY_MISC_INFO'
    
    SYMBOL = Column(String(10), nullable=False)
    TIME_STAMP = Column(Date, nullable = False)
    
    FF_MKT_CAP_CR = Column(Float, nullable = True) #: free-float market-cap in crores
    D2T_PCT = Column(Float, nullable = True) #: delivery percentage. % of shares which were not squared off the same day out of total shares traded
    
    LOWER_PX_BAND = Column(Float, nullable = True) #: trading is halted if the stock trades below this level
    UPPER_PX_BAND = Column(Float, nullable = True) #: trading is halted if the stock trades above this level
    
    __table_args__ = (PrimaryKeyConstraint('SYMBOL', 'TIME_STAMP'),)
    
    def __repr__(self):
        return f"{self.SYMBOL}/{self.TIME_STAMP.strftime('%Y-%b-%d')}: {self.FF_MKT_CAP_CR},{self.D2T_PCT},{self.LOWER_PX_BAND},{self.UPPER_PX_BAND}"

class MarketCapDecile(Base, StockViz):
    """Query market-cap decile of of listed equity tickers"""
    
    __tablename__ = 'DECILE_CONSTITUENTS'
    
    SYMBOL = Column(String(10), nullable=False)
    TIME_STAMP = Column(Date, nullable = False)
    DECILE = Column(Integer, nullable = False)
    
    __table_args__ = (PrimaryKeyConstraint('SYMBOL', 'TIME_STAMP', 'DECILE'),)
    
    def __repr__(self):
        return f"{self.SYMBOL}/{self.TIME_STAMP.strftime('%Y-%b-%d')}: {self.DECILE}"
            
class EodTimeSeries(Base, StockViz):
    """Query unadjusted end-of-day price and volume time-series for listed stocks"""
    
    __tablename__ = 'PX_HISTORY'
    
    SYMBOL = Column(String(10), nullable=False) 
    SERIES = Column(String(5), nullable=False) 
    TIME_STAMP = Column(Date, nullable = False)
    
    HIGH = Column('PX_HIGH', Float, nullable=True)
    LOW = Column('PX_LOW', Float, nullable=True)
    OPEN = Column('PX_OPEN', Float, nullable=True)
    CLOSE = Column('PX_CLOSE', Float, nullable=True) #: usually a weighted average of price x volume of the last 15-minutes of trading
    LAST = Column('PX_LAST', Float, nullable=True) #: last traded price
    
    VOLUME = Column('TOT_TRD_QTY', Float, nullable=True) 
    
    __table_args__ = (PrimaryKeyConstraint('SYMBOL', 'SERIES', 'TIME_STAMP'),)
    
    def __repr__(self):
        return f"{self.SYMBOL}({self.SERIES})/{self.TIME_STAMP.strftime('%Y-%b-%d')}: {self.HIGH},{self.LOW},{self.OPEN},{self.CLOSE},{self.VOLUME}"

class EodAdjustedTimeSeries(Base, StockVizDyn):
    """Query end-of-day price and volume time-series adjusted for splits, bonus and dividends for listed stocks"""
    
    __tablename__ = 'eod_adjusted_nse'
    
    SYMBOL = Column('ticker', String(50), nullable=False) 
    TIME_STAMP = Column('date_stamp', IntegerDate, nullable = False)
    
    HIGH = Column('h', Float, nullable=True)
    LOW = Column('l', Float, nullable=True)
    OPEN = Column('o', Float, nullable=True)
    CLOSE = Column('c', Float, nullable=True)
    
    VOLUME = Column('v', Float, nullable=True) 
    
    __table_args__ = (PrimaryKeyConstraint('ticker', 'date_stamp'),)
    
    def __repr__(self):
        return f"{self.SYMBOL}/{self.TIME_STAMP.strftime('%Y-%b-%d')}: {self.HIGH},{self.LOW},{self.OPEN},{self.CLOSE},{self.VOLUME}"
    
class DailyReturns(Base, StockViz):
    """Query the percentage daily return (close-to-close) time-series for listed stocks"""    
    
    __tablename__ = 'RETURN_SERIES_ALL'
    
    SYMBOL = Column(String(10), nullable=False) 
    TIME_STAMP = Column(Date, nullable = False)
    VALUE = Column('DAILY_RETURN', Float, nullable=True)
    
    __table_args__ = (PrimaryKeyConstraint('SYMBOL', 'TIME_STAMP'),)
    
    def __repr__(self):
        return f"{self.SYMBOL}/{self.TIME_STAMP.strftime('%Y-%b-%d')}: {self.VALUE}"
    
class CorporateActions(Base, StockViz):
    """Query the corporate actions for listed stocks"""
    
    __tablename__ = 'CORP_ACTION'
    
    SYMBOL = Column(String(10), nullable=False) 
    SERIES = Column(String(5), nullable=False)
    EX_DATE = Column(Date, nullable = False)
    
    PURPOSE = Column(String(256), nullable=False)
    
    WHEN_UPDATED = Column('UPDATE_DT', Date, nullable=False) 
    
    __table_args__ = (PrimaryKeyConstraint('SYMBOL', 'SERIES', 'EX_DATE'),)
    
    def __repr__(self):
        return f"{self.SYMBOL}({self.SERIES})/{self.EX_DATE.strftime('%Y-%b-%d')}: {self.PURPOSE}"
    
class CorporateResultsMeta(Base, StockViz):
    """Query to obtain the REF_ID to lookup CorporateResults for a specific period"""
    
    __tablename__ = 'CORP_RESULTS_KEY_NSE'
    
    REF_ID = Column('AUTO_ID', BigInteger, primary_key=True, nullable=False) #: use this to query CorporateResults
    
    SYMBOL = Column(String(10), nullable=False)
    IS_AUDITED = Column(Boolean, nullable=False)
    IS_CUMULATIVE = Column(Boolean, nullable=False)
    IS_CONSOLIDATED = Column(Boolean, nullable=False)
    
    PERIOD_BEGIN = Column(Date, nullable=False)
    PERIOD_END = Column(Date, nullable=False)
    PERIOD = Column('PERIOD_KEY', String(50), nullable=False)
    
    BROADCAST_DATE = Column('BROADCAST_STAMP', Date, nullable=False)
    
    def __repr__(self):
        return f"{self.SYMBOL}({self.IS_AUDITED}/{self.IS_CUMULATIVE}/{self.IS_CONSOLIDATED}) [{self.PERIOD}: {self.PERIOD_BEGIN.strftime('%Y-%b-%d')} ~ {self.PERIOD_END.strftime('%Y-%b-%d')}]"
    
class CorporateResults(Base, StockViz):
    """Query to CorporateResults for a specific period and stock"""

    __tablename__ = 'CORP_RESULTS_QTR_NSE'
    
    REF_ID = Column(BigInteger, nullable=False) #: lookup CorporateResultsMeta to get this value
    
    H1 = Column(String(254), nullable=True) #: section 1
    H2 = Column(String(254), nullable=True) #: section 2
    H3 = Column(String(254), nullable=True) #: section 3
    H4 = Column(String(254), nullable=True) #: section 4
    
    KEY = Column('K', String(254), nullable=False)
    VALUE = Column('V', Float, nullable = False)
    
    AUTO_ID = Column(BigInteger, primary_key=True, nullable=False)
    
    def __repr__(self):
        return f"{self.H1}/{self.H2}/{self.H3}/{self.H4}/{self.KEY}: {self.VALUE}"