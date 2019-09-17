"""ETFs listed in the US

.. module:: ETFsUs
    :synopsis: Query US ETF information from various sources
"""

from sqlalchemy import Column, Integer, BigInteger, String, Date, Float, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from datetime import date, datetime

from .Db import StockViz

Base = declarative_base()

class Meta(Base, StockViz):
    """Query the meta-data"""
    
    __tablename__ = 'ETF_META_V'
    
    SYMBOL = Column(String(10), nullable=False, primary_key=True)
    NAME = Column('FUND', String(254), nullable=False)
    
    LAUNCH_DATE = Column(Date, nullable=True)
    ISSUER = Column(String(126), nullable=True)
    EXPENSE_RATIO = Column(Float, nullable=True)
    AUM = Column(BigInteger, nullable=True)
    
    ASSET_CLASS = Column(String(50), nullable=True)
    SEGMENT = Column(String(254), nullable=True)
    UNDERLYING_INDEX = Column(String(254), nullable=True)

    def __repr__(self):
        return f"{self.SYMBOL}/{self.NAME}: {self.ASSET_CLASS} ~ {self.UNDERLYING_INDEX} since {self.LAUNCH_DATE}"
