"""This example illustrates how to use the InvestmentFlowsIndia data-set."""

import sys
sys.path.append("..")

import pandas as pd    
from sqlalchemy import func, and_, or_, text, Integer
from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import cast
from plutoPy.model import RoutingSession, InvestmentFlowsIndia
from datetime import date, datetime, timedelta

# get daily DII and FII flows for the last 20 days for the cash market

print("daily DII and FII flows for the last 20 days for the cash market:")

results = (RoutingSession.session.query(InvestmentFlowsIndia.DiiCashMarket.TIME_STAMP, InvestmentFlowsIndia.DiiCashMarket.SECURITY_TYPE,
                                        func.sum(InvestmentFlowsIndia.DiiCashMarket.BUY_VALUE + InvestmentFlowsIndia.FiiCashMarket.BUY_VALUE).label('BUY'), 
                                        func.sum(InvestmentFlowsIndia.DiiCashMarket.SELL_VALUE + InvestmentFlowsIndia.FiiCashMarket.SELL_VALUE).label('SELL'),
                                        func.sum(InvestmentFlowsIndia.DiiCashMarket.BUY_VALUE + InvestmentFlowsIndia.FiiCashMarket.BUY_VALUE
                                         - InvestmentFlowsIndia.DiiCashMarket.SELL_VALUE - InvestmentFlowsIndia.FiiCashMarket.SELL_VALUE).label('NET'))
            .outerjoin(InvestmentFlowsIndia.FiiCashMarket, and_(InvestmentFlowsIndia.FiiCashMarket.TIME_STAMP == InvestmentFlowsIndia.DiiCashMarket.TIME_STAMP,
                                                                InvestmentFlowsIndia.FiiCashMarket.SECURITY_TYPE == InvestmentFlowsIndia.DiiCashMarket.SECURITY_TYPE))
            .group_by(InvestmentFlowsIndia.DiiCashMarket.TIME_STAMP, InvestmentFlowsIndia.DiiCashMarket.SECURITY_TYPE)
            .order_by(InvestmentFlowsIndia.DiiCashMarket.TIME_STAMP.desc())
            .limit(20)
            .all())

for instance in results:
    print(instance)
    
# get instruments traced for DIIs in the derivative market   

print("instruments traced for DIIs in the derivative market") 

results = (RoutingSession.session.query(InvestmentFlowsIndia.DiiDerivativesMarket.SECURITY_TYPE,
                                        func.min(InvestmentFlowsIndia.DiiDerivativesMarket.TIME_STAMP).label('start_dt'),
                                        func.max(InvestmentFlowsIndia.DiiDerivativesMarket.TIME_STAMP).label('end_dt'))
            .group_by(InvestmentFlowsIndia.DiiDerivativesMarket.SECURITY_TYPE)
            .order_by(text('start_dt'))
            .all())

for instance in results:
    print(instance)
    
# get instruments traced for FIIs in the derivative market   

print("instruments traced for FIIs in the derivative market") 

results = (RoutingSession.session.query(InvestmentFlowsIndia.FiiDerivativesMarket.SECURITY_TYPE,
                                        func.min(InvestmentFlowsIndia.FiiDerivativesMarket.TIME_STAMP).label('start_dt'),
                                        func.max(InvestmentFlowsIndia.FiiDerivativesMarket.TIME_STAMP).label('end_dt'))
            .group_by(InvestmentFlowsIndia.FiiDerivativesMarket.SECURITY_TYPE)
            .order_by(text('start_dt'))
            .all())

for instance in results:
    print(instance)
    
