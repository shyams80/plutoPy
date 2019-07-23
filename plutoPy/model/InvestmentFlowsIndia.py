"""Investment Flows India

sources: http://www.cdslindia.com https://www.sebi.gov.in 

.. module:: InvestmentFlowsIndia
    :synopsis: Query information about investment flows in to and out of Indian capital markets
"""

from sqlalchemy import Column, Integer, BigInteger, String, Date, DateTime, Float, Boolean, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from datetime import date, datetime

from .Db import StockViz

Base = declarative_base()

class DiiCashMarket(Base, StockViz):
    """Query purchases and sales of debt and equity by Domestic Institutional Investors"""
    
    __tablename__ = 'DII_MKT_FLOW'
    
    TIME_STAMP = Column('AsOf', Date, nullable = False)
    SECURITY_TYPE = Column('SecType', String(50), nullable = False)
    
    BUY_VALUE = Column('Purchases', Float, nullable = False) #: in Rs.
    SELL_VALUE = Column('Sales', Float, nullable = False) #: in Rs.
    
    __table_args__ = (PrimaryKeyConstraint('SecType', 'AsOf'),)
    
    def __repr__(self):
        return f"{self.SECURITY_TYPE}/{self.TIME_STAMP.strftime('%Y-%b-%d')}: {self.BUY_VALUE},{self.SELL_VALUE}"
    
class DiiDerivativesMarket(Base, StockViz):
    """Query purchases and sales of futures and options by Domestic Institutional Investors"""
    
    __tablename__ = 'DII_DERIV_FLOW'
    
    TIME_STAMP = Column('AsOf', Date, nullable = False)
    SECURITY_TYPE = Column('DerivProduct', String(50), nullable = False)
    
    BUY_CONTRACTS = Column('BuyContracts', Float, nullable = False)
    BUY_VALUE = Column('BuyAmount', Float, nullable = False) #: in Rs.
    
    SELL_CONTRACTS = Column('SellContracts', Float, nullable = False)
    SELL_VALUE = Column('SellAmount', Float, nullable = False) #: in Rs.
    
    OI_CONTRACTS = Column('OIContracts', Float, nullable = False)
    OI_VALUE = Column('OIAmount', Float, nullable = False) #: in Rs.
    
    __table_args__ = (PrimaryKeyConstraint('DerivProduct', 'AsOf'),)
    
    def __repr__(self):
        return f"{self.SECURITY_TYPE}/{self.TIME_STAMP.strftime('%Y-%b-%d')}: {self.OI_CONTRACTS},{self.OI_VALUE}"
    
class FiiCashMarket(Base, StockViz):
    """Query purchases and sales of debt and equity by Foreign Institutional Investors"""
    
    __tablename__ = 'FII_MKT_FLOW'
    
    TIME_STAMP = Column('AsOf', Date, nullable = False)
    SECURITY_TYPE = Column('SecType', String(50), nullable = False)
    ROUTE = Column('Route', String(50), nullable = False) #: Stock Exchange OR Primary market
    
    BUY_VALUE = Column('Purchases', Float, nullable = False) #: in Rs.
    SELL_VALUE = Column('Sales', Float, nullable = False) #: in Rs.
    
    NET_VALUE_DLR = Column('NetDlr', Float, nullable = False) #: net flow in USD
    CONVERSION_RATE_USDINR = Column('ConverionRate', Float, nullable = False)
    
    __table_args__ = (PrimaryKeyConstraint('SecType', 'AsOf', 'Route'),)
    
    def __repr__(self):
        return f"{self.SECURITY_TYPE}/{self.ROUTE}/{self.TIME_STAMP.strftime('%Y-%b-%d')}: {self.NET_VALUE_DLR}"
    
class FiiDerivativesMarket(Base, StockViz):
    """Query purchases and sales of futures and options by Foreign Institutional Investors"""
    
    __tablename__ = 'FII_DERIV_FLOW'
    
    TIME_STAMP = Column('AsOf', Date, nullable = False)
    SECURITY_TYPE = Column('DerivProduct', String(50), nullable = False)
    
    BUY_CONTRACTS = Column('BuyContracts', Float, nullable = False)
    BUY_VALUE = Column('BuyAmount', Float, nullable = False) #: in Rs.
    
    SELL_CONTRACTS = Column('SellContracts', Float, nullable = False)
    SELL_VALUE = Column('SellAmount', Float, nullable = False) #: in Rs.
    
    OI_CONTRACTS = Column('OIContracts', Float, nullable = False)
    OI_VALUE = Column('OIAmount', Float, nullable = False) #: in Rs.
    
    __table_args__ = (PrimaryKeyConstraint('DerivProduct', 'AsOf'),)
    
    def __repr__(self):
        return f"{self.SECURITY_TYPE}/{self.TIME_STAMP.strftime('%Y-%b-%d')}: {self.OI_CONTRACTS},{self.OI_VALUE}"         