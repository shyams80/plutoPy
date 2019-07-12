"""Yield curves

sources: https://www.ccilindia.com http://treasury.gov https://www.ecb.europa.eu

.. module:: YieldCurve
    :synopsis: Query yield curves from across the world
"""

from sqlalchemy import Column, Integer, String, Date, Float, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from datetime import date, datetime

from .Db import StockViz

Base = declarative_base()

class IndiaZeroCoupon(Base, StockViz):
    """Query the Indian Zero Coupon Yield Curve published by CCIL"""
    
    __tablename__ = 'ZERO_COUPON_CURVE'
    
    TIME_STAMP = Column(Date, nullable=False)
    
    MATURITY = Column(Float, nullable=False)
    YIELD = Column(Float, nullable=False)
    
    __table_args__ = (PrimaryKeyConstraint('TIME_STAMP', 'MATURITY'),)
    
    def __repr__(self):
        return f"{self.TIME_STAMP.strftime('%Y-%b-%d')}: {self.MATURITY}, {self.YIELD}"
    

class UsTreasury(Base, StockViz):
    """Query the Daily Treasury Yield Curve Rates published by US Treasury"""
    
    __tablename__ = 'UST_YIELD_CURVE'
    
    TIME_STAMP = Column(Date, primary_key=True, nullable=False)
    
    M1 = Column(Float, nullable=True) #: 'M' implies month
    M3 = Column(Float, nullable=True)
    M6 = Column(Float, nullable=True)
    
    Y1 = Column(Float, nullable=True) #: 'Y' implies year
    Y2 = Column(Float, nullable=True)
    Y3 = Column(Float, nullable=True)
    Y5 = Column(Float, nullable=True)
    Y7 = Column(Float, nullable=True)
    Y10 = Column(Float, nullable=True)
    Y20 = Column(Float, nullable=True)
    Y30 = Column(Float, nullable=True)
    
    def __repr__(self):
        return f"{self.TIME_STAMP.strftime('%Y-%b-%d')}: {self.M1} --> {self.Y30}"
    
class EuroArea(Base, StockViz): 
    """Query Euro area yield curves published by the ECB"""   
    
    __tablename__ = 'EUR_YIELD_CURVE'
    
    CURVE_ID = Column(String(5), nullable=False) #: G_N_A for AAA rated only. G_N_C for all (including AAA) rated.
    TIME_STAMP = Column(Date, nullable=False)
    
    TENOR_Y = Column(Integer, nullable=False) #: year
    TENOR_M = Column(Integer, nullable=False) #: month
    
    VALUE = Column('VAL', Float, nullable=False) #: yield
    
    __table_args__ = (PrimaryKeyConstraint('CURVE_ID', 'TIME_STAMP', 'TENOR_Y', 'TENOR_M'),)
    
    def __repr__(self):
        return f"{self.TIME_STAMP.strftime('%Y-%b-%d')}/{self.CURVE_ID}: {self.TENOR_Y}+{self.TENOR_M}, {self.VALUE}"
    
