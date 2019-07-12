"""World Bank Global Economic Monitor data

sources: https://worldbank.org

.. module:: WorldBank
    :synopsis: Query World Bank Global Economic Monitor data
"""

from sqlalchemy import Column, Integer, String, Date, Float, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from datetime import date, datetime

from .Db import StockVizUs

Base = declarative_base()

class Meta(Base, StockVizUs):
    """Query to find the country and indicator id's of the Global Economic Monitor data published by the World Bank"""     
    
    __tablename__ = 'WORLD_BANK_META'
    
    COUNTRY_ID = Column(String(5), nullable=False)
    COUNTRY_NAME = Column(String(510), nullable=False)
    
    INDICATOR_ID = Column(String(50), nullable=False)
    INDICATOR_NAME = Column(String(510), nullable=False)
   
    COUNTRY_KEY = Column('C_ID', Integer, nullable=False) #: COUNTRY_KEY and INDICATOR_KEY uniquely identify a time-series
    INDICATOR_KEY = Column('I_ID', Integer, nullable=False) #: COUNTRY_KEY and INDICATOR_KEY uniquely identify a time-series
    
    START_YEAR = Column('SY', Integer, nullable=False) #: starting year from which time-series is available
    END_YEAR = Column('EY', Integer, nullable=False) #: ending year from which time-series is available
    
    __table_args__ = (PrimaryKeyConstraint('C_ID', 'I_ID'),)
    
    def __repr__(self):
        return f"{self.COUNTRY_NAME}/{self.INDICATOR_NAME}: {self.COUNTRY_KEY}/{self.INDICATOR_KEY} ~ {self.START_YEAR} - {self.END_YEAR}"
    
class TimeSeries(Base, StockVizUs): 
    """Query the Global Economic Monitor data the World Bank""" 
    
    __tablename__ = 'WORLD_BANK_OBSERVATION'   
    
    COUNTRY_KEY = Column('COUNTRY_ID', Integer, nullable=False) #: COUNTRY_KEY and INDICATOR_KEY uniquely identifies the time-series
    INDICATOR_KEY = Column('INDICATOR_ID', Integer, nullable=False) #: COUNTRY_KEY and INDICATOR_KEY uniquely identifies the time-series
    
    YEAR = Column(Integer, nullable=False)
    VALUE = Column(Float, nullable=False)
    
    __table_args__ = (PrimaryKeyConstraint('COUNTRY_ID', 'INDICATOR_ID', 'YEAR'),)
    
    def __repr__(self):
        return f"{self.YEAR}: {self.VALUE}"