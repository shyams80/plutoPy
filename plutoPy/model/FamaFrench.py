"""Fama French Data-sets

source: http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/index.html

.. module:: FamaFrench
    :synopsis: Query Fama-French time-series
"""

from sqlalchemy import Column, Integer, String, Date, Float, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from datetime import date, datetime

from .Db import StockVizUs2

Base = declarative_base()

class FiveFactor3x2Daily(Base, StockVizUs2):
    """Query the Fama-French 5-factor daily returns (http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_5_factors_2x3.html)"""    
    
    __tablename__ = "FAMA_FRENCH_5_FACTOR_DAILY"
    
    TIME_STAMP = Column(Date, nullable=False)
    KEY_ID = Column(String(50), nullable=False) #: SMB, RMW, RF, MKT-RF, HML, CMA
    
    RET = Column(Float, nullable=True)
    
    __table_args__ = (PrimaryKeyConstraint('KEY_ID', 'TIME_STAMP'),)
    
    def __repr__(self):
        return f"{self.TIME_STAMP.strftime('%Y-%b-%d')}, {self.KEY_ID}: {self.RET}"
    
class Industry49Daily(Base, StockVizUs2):
    """Query the Fama-French daily returns of 49 different industries (http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/det_49_ind_port.html)"""    
    
    __tablename__ = "FAMA_FRENCH_INDUSTRY_49_DAILY"
    
    TIME_STAMP = Column(Date, nullable=False)
    KEY_ID = Column(String(50), nullable=False) #: AGRIC, BANKS, CHEMS, etc... 
    RET_TYPE = Column(String(50), nullable=False) #: AVWRD - Average Value Weighted Returns Daily, AEWRD - Average Equal Weighted Returns Daily
    
    RET = Column(Float, nullable=True)
    
    __table_args__ = (PrimaryKeyConstraint('KEY_ID', 'TIME_STAMP', 'RET_TYPE'),)
    
    def __repr__(self):
        return f"{self.TIME_STAMP.strftime('%Y-%b-%d')}, {self.KEY_ID}, {self.RET_TYPE}: {self.RET}"    

class MomentumDaily(Base, StockVizUs2):
    """Query the Fama-French daily returns of momentum factor and portfolios
    factor: https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/det_mom_factor_daily.html
    portfolios: https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/det_10_port_form_pr_12_2_daily.html
    """    
    
    __tablename__ = "FAMA_FRENCH_MOMENTUM_DAILY"
    
    TIME_STAMP = Column(Date, nullable=False)
    KEY_ID = Column(String(50), nullable=False) #: MOM, HI_PRIOR, LO_PRIOR, PRIOR_[2..9]
    RET_TYPE = Column(String(50), nullable=False) #: M for KEY_ID = MOM, AVWRD - Average Value Weighted Returns Daily, AEWRD - Average Equal Weighted Returns Daily
    
    RET = Column(Float, nullable=True)
    
    __table_args__ = (PrimaryKeyConstraint('KEY_ID', 'TIME_STAMP', 'RET_TYPE'),)
    
    def __repr__(self):
        return f"{self.TIME_STAMP.strftime('%Y-%b-%d')}, {self.KEY_ID}, {self.RET_TYPE}: {self.RET}" 
    
class MomentumMonthly(Base, StockVizUs2):
    """Query the Fama-French daily returns of momentum factor and portfolios
    factor: https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/det_mom_factor.html
    portfolios: https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/det_10_port_form_pr_12_2.html
    """    
    
    __tablename__ = "FAMA_FRENCH_MOMENTUM_MONTHLY"
    
    TIME_STAMP = Column(Date, nullable=False)
    KEY_ID = Column(String(50), nullable=False) #: MOM, HI_PRIOR, LO_PRIOR, PRIOR_[2..9]
    RET_TYPE = Column(String(50), nullable=False) #: M for KEY_ID = MOM, AVWRD - Average Value Weighted Returns Daily, AEWRD - Average Equal Weighted Returns Daily
    
    RET = Column(Float, nullable=True)
    
    __table_args__ = (PrimaryKeyConstraint('KEY_ID', 'TIME_STAMP', 'RET_TYPE'),)
    
    def __repr__(self):
        return f"{self.TIME_STAMP.strftime('%Y-%b-%d')}, {self.KEY_ID}, {self.RET_TYPE}: {self.RET}" 
        