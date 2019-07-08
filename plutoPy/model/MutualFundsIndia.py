"""Mutual Funds India

sources: https://www.amfiindia.com/

.. module:: MutualFundsIndia
    :synopsis: Query Indian mutual fund information from various sources
"""

from sqlalchemy import Column, Integer, BigInteger, String, Date, Float, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from datetime import date, datetime

from .Db import StockViz

Base = declarative_base()

class Meta(Base, StockViz):
    """Query the meta-data"""
    
    __tablename__ = 'MF_META2'
    
    SCHEME_CODE = Column(Integer, nullable=False) #: code given by AMFI
    AS_OF = Column(Date, nullable=False) #: data capture date
    
    BENCH_ORIG = Column(String(510), nullable=True) #: original benchmark
    BENCH_NOW = Column(String(510), nullable=True) #: benchmark being used currently
    CATEGORY = Column(String(510), nullable=True) #: Mid-Cap, Index Funds, etc...
    EXPENSE = Column(Float, nullable=True) #: Based on prospectus (%)
    EXPENSE_RATIO = Column(Float, nullable=True) #: Based on what the fund actually charged (%)
    TURNOVER_RATIO = Column(Float, nullable=True) #: churn

    __table_args__ = (PrimaryKeyConstraint('SCHEME_CODE', 'AS_OF'),)
    
    def __repr__(self):
        return f"{self.AS_OF.strftime('%Y-%b-%d')},{self.SCHEME_CODE}: {self.BENCH_ORIG} ~ {self.CATEGORY}"

class AumFundwise(Base, StockViz):
    """Query the fund-wise assets under management (AUM) of different asset managers"""
    
    __tablename__ = 'MF_FUNDWISE_AUM'
    
    AUTO_ID = Column(Integer, primary_key=True, nullable=False)
    
    PERIOD = Column(Date, nullable=False)
    FUND = Column(String(50), nullable=False) #: name of the manager
    AVG_AUM_WO_FOFD = Column(Float, nullable=False) #: excluding AUM held by Fund-of-Funds
    AVG_AUM_FOFD = Column(Float, nullable=False) #: AUM held by Fund-of-Funds

    def __repr__(self):
        return f"{self.PERIOD.strftime('%Y-%b-%d')},{self.FUND}: {self.AVG_AUM_WO_FOFD + self.AVG_AUM_FOFD}"

class AumSchemewise(Base, StockViz):
    """Query the scheme-wise assets under management (AUM) of different asset managers and their 'schemes'"""
    
    __tablename__ = 'MF_SCHEMEWISE_AUM'
    
    AUTO_ID = Column(BigInteger, primary_key=True, nullable=False)
    
    PERIOD = Column(Date, nullable=False)
    SCHEME_CODE = Column('AMFI_CODE', Integer, nullable=False) #: code given by AMFI
    SCHEME_NAME = Column(String(254), nullable=False) #: name of the fund - can change multiple times over its life
    
    AVG_AUM_WO_FOFD = Column(Float, nullable=False) #: excluding AUM held by Fund-of-Funds
    AVG_AUM_FOFD = Column(Float, nullable=False) #: AUM held by Fund-of-Funds

    def __repr__(self):
        return f"{self.PERIOD.strftime('%Y-%b-%d')},{self.SCHEME_NAME (self.SCHEME_CODE)}: {self.AVG_AUM_WO_FOFD + self.AVG_AUM_FOFD}"
    
class NavTimeSeries(Base, StockViz):
    """Query for the NAVs of different funds"""
    
    __tablename__ = 'MF_NAV_HISTORY'
    
    SCHEME_CODE = Column(Integer, nullable=False) #: code given by AMFI
    TIME_STAMP = Column('AS_OF', Date, nullable=False) #: mostly daily but some funds declare only twice a week. bond market holidays are different from equity market holidays.
    
    SCHEME_NAME = Column(String(254), nullable=False) #: name of the fund - can change multiple times over its life
    NAV = Column(Float, nullable=False) #: before exit loads, STT, etc...

    __table_args__ = (PrimaryKeyConstraint('SCHEME_CODE', 'AS_OF'),)
    
    def __repr__(self):
        return f"{self.TIME_STAMP.strftime('%Y-%b-%d')},{self.SCHEME_NAME (self.SCHEME_CODE)}: {self.NAV}"  
    
class Portfolio(Base, StockViz):
    """Query for the monthly reported portfolios of different funds"""
    
    __tablename__ = 'MF_PORTFOLIO_HISTORY'
    
    AUTO_ID = Column(BigInteger, primary_key=True, nullable=False)
    
    SCHEME_CODE = Column(Integer, nullable=False) #: code given by AMFI
    PORTFOLIO_DATE = Column(Date, nullable=False) #: mostly declared once a month. available after the 10th of each month.
    
    INSTRUMENT = Column(String(50), nullable=False) #: EQUITY, BOND, OTHER... broad classification
    INSTRUMENT_TYPE = Column(String(50), nullable=False) #: E, BT, CR... clarifies INSTRUMENT
    
    SYMBOL = Column(String(50), nullable=True) #: where available, the NSE ticker/symbol of the position
    NAME = Column(String(510), nullable=False) #: name of the position
    SECTOR = Column(String(50), nullable=True) #: BASIC MATERIALS, FINANCIAL SERVICES, CONSUMER DEFENSIVE, etc...
    INDUSTRY_BSE = Column(String(254), nullable=True) #: BSE's SECTOR classification.
    
    WEIGHTAGE = Column(Float, nullable=True) #: weightage of the position in the portfolio (%)

    def __repr__(self):
        return f"{self.PORTFOLIO_DATE.strftime('%Y-%b-%d')},{self.SCHEME_CODE}: {self.INSTRUMENT}/{self.INSTRUMENT_TYPE} ~ {self.NAME}: {self.WEIGHTAGE}"  