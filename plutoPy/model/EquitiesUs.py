"""Equities US

sources: https://iexcloud.io https://www.sec.gov/

.. module:: EquitiesUs
    :synopsis: Query information about equities listed in the United States 
"""

from sqlalchemy import Column, Integer, BigInteger, String, Date, Float, Boolean, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from datetime import date, datetime

from .Db import StockVizUs2

Base = declarative_base()

class Tickers(Base, StockVizUs2):
    """Query meta data of listed equity (common stock) tickers"""
    
    __tablename__ = 'EQUITY_TICKER_US'
    
    SYMBOL = Column(String(50), nullable=False, primary_key=True) #: ticker/stock symbol. for eg: AAPL
    NAME = Column('CO_NAME', String(254), nullable=False) #: name of the company
    
    EXCHANGE = Column('EXCH', String(254), nullable=True) #: listed exchange
    
    MKT_CAP = Column(Float, nullable=True) #: market cap in USD
    
    def __repr__(self):
        return f"{self.SYMBOL}/{self.NAME}/{self.EXCHANGE}"
    
class EodAdjustedTimeSeries(Base, StockVizUs2):
    """Query end-of-day price and volume time-series adjusted for splits, bonus and dividends for listed stocks"""
    
    __tablename__ = 'BHAV_EQ_TD'
    
    SYMBOL = Column(String(10), nullable=False) 
    TIME_STAMP = Column(Date, nullable = False)
    
    HIGH = Column('H', Float, nullable=True)
    LOW = Column('L', Float, nullable=True)
    OPEN = Column('O', Float, nullable=True)
    CLOSE = Column('C', Float, nullable=True)
    
    VOLUME = Column('V', Float, nullable=True) 
    
    __table_args__ = (PrimaryKeyConstraint('SYMBOL', 'TIME_STAMP'),)
    
    def __repr__(self):
        return f"{self.SYMBOL}/{self.TIME_STAMP}: {self.HIGH},{self.LOW},{self.OPEN},{self.CLOSE},{self.VOLUME}"
        
class SecMeta(Base, StockVizUs2):
    """Meta information of companies in the SEC EDGAR database. Useful for SIC."""
    
    __tablename__ = 'SEC_META'   
    
    SYMBOL = Column('TICKER', String(50), nullable=False, primary_key=True) 
    NAME = Column(String(254), nullable=False)
    
    CIK = Column(String(10), nullable=False) #: Central Index Key
    SIC = Column(Integer, nullable=False) #: Standard Industrial Classification code
    SIC_DESC = Column(String(254), nullable=False) #: Standard Industrial Classification
    
    def __repr__(self):
        return f"{self.SYMBOL}/{self.NAME}/{self.SIC_DESC}"
    
class SecFilings(Base, StockVizUs2):
    """Links to SEC filings. Useful to keep track of M&A events in your portfolio"""    
    
    __tablename__ = 'SEC_FILINGS'
    
    ACC_NO = Column(String(50), nullable=False)
    SYMBOL = Column('TICKER', String(10), nullable=False)   
     
    FILING_DATE = Column(Date, nullable=False)
    FILING_URL = Column(String(254), nullable=False)
    FILING_TYPE = Column(String(50), nullable=False) #: SC14D9C => acquisitions; DEFM14A => mergers
    FORM_NAME = Column(String(510), nullable=False)
    
    __table_args__ = (PrimaryKeyConstraint('ACC_NO', 'TICKER'),)
    
    def __repr__(self):
        return f"{self.SYMBOL}/{self.FILING_DATE}/{self.FILING_TYPE}"
    
         