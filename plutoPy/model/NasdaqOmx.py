"""NASDAQOMX Indices

sources: https://indexes.nasdaqomx.com/ https://www.quandl.com/

.. module:: NasdaqOmx
    :synopsis: Query NASDAQOMX total-return (TR) index time-series
"""

from sqlalchemy import Column, Integer, String, Date, Float, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from datetime import date, datetime

from .Db import StockVizUs2

Base = declarative_base()

class Meta(Base, StockVizUs2):
    """Query to find the time-series id of total-return indices published by the NasdaqOmx"""     
    
    __tablename__ = 'NASDAQOMX_META'
    
    ID = Column(Integer, primary_key=True, nullable=False) #: time-series id to be used to query NasdaqOmxTimeSeries
    CODE = Column('DATASET_CODE', String(50), nullable=False) #: NasdaqOmx index code
    NAME = Column('INDEX_NAME', String(510), nullable=False) #: name of the index
    
    def __repr__(self):
        return f"{self.ID}/{self.CODE}: {self.NAME}"
    
class TimeSeries(Base, StockVizUs2): 
    """Query the index time-series published by the NasdaqOmx""" 
    
    __tablename__ = 'QUANDL_DATA_V3'   
    
    ID = Column(Integer, nullable=False) #: time-series id
    TIME_STAMP = Column('TRADE_DATE', Date, nullable=False)
    
    CLOSE = Column('INDEX_VALUE', Float, nullable=False)
    
    __table_args__ = (PrimaryKeyConstraint('ID', 'TRADE_DATE'),)
    
    def __repr__(self):
        return f"{self.TIME_STAMP}: {self.CLOSE}"