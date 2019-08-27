"""International Monetary Fund data

sources: https://www.imf.org

.. module:: InternationalMonetaryFund
    :synopsis: Query International Monetary Fund data
"""

from sqlalchemy import Column, Integer, String, Date, Float, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from datetime import date, datetime

from .Db import StockVizUs

Base = declarative_base()

class Meta(Base, StockVizUs):
    """Query IMF meta-data based on geography/indicator. Then use the ID obtained here to query the time-series"""
    
    __tablename__ = 'IMF_META'
    
    ID = Column(Integer, primary_key=True, nullable=False) #: use to query TimeSeries
    
    AREA_CODE = Column(String(62), nullable=False) #: IN, GB, US...
    AREA = Column(String(254), nullable=False) #: India, Great Britain, United States
    
    DATA_KEY = Column(String(30), nullable=False) #: IMF internal key: PCOPP, AIP_IX
    DATA_DESCRIPTION = Column(String(510), nullable=False) #: description of the data: 'Primary Commodity Prices, Copper', 'Economic Activity, Industrial Production, Index' 
    
    FREQ = Column(String(6), nullable=False) #: A for Annual; Q for Quarterly; M for Monthly
    UNIT_MEASURE = Column(String(6), nullable=True) #: IX for Index; USD for Dollar
    UNIT_MULT = Column(Float, nullable=True) #: 0, 3, 6 to multiply by none, thousands and millions
    
    START_YEAR = Column(Integer, nullable=False) #: the year from which TimeSeries data is available
    END_YEAR = Column(Integer, nullable=False) #: the year till which TimeSeries data is available
    
    def __repr__(self):
        return f"{self.ID}/{self.AREA_CODE}/{self.AREA}::{self.DATA_KEY}/{self.DATA_DESCRIPTION} ~ {self.FREQ} {self.START_YEAR}-{self.END_YEAR}"
    
class TimeSeries(Base, StockVizUs):
    """Query the IMF time-series data based on the Meta ID"""
    
    __tablename__ = 'IMF_OBSERVATION'
    
    AUTO_ID = Column(Integer, primary_key=True, nullable=False)
    ID = Column('SERIES_ID', Integer, nullable=False) #: get this from Meta
    YEAR = Column('DATE_Y', Integer, nullable=False)
    MONTH = Column('DATE_M', Integer, nullable=True)
    VALUE = Column('VAL', Float, nullable=False)
    
    def __repr__(self):
        return f"{self.YEAR}.{self.MONTH}: {self.VALUE}"
        
