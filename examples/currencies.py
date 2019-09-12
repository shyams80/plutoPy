"""This example illustrates how to use the Currencies data-set."""

import sys
sys.path.append("..")

import pandas as pd    
from sqlalchemy import func, and_, or_, text, Integer
from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import cast
from plutoPy.model import RoutingSession, Currencies
from datetime import date, datetime, timedelta

print("AlphaVantage end-of-day pairs:")

results = (RoutingSession.session.query(Currencies.AvEodTimeSeries.SYMBOL, 
                                        func.min(Currencies.AvEodTimeSeries.TIME_STAMP).label('start_dt'), 
                                        func.max(Currencies.AvEodTimeSeries.TIME_STAMP).label('end_dt'))
            .group_by(Currencies.AvEodTimeSeries.SYMBOL)
            .order_by(text('start_dt'))).all()

for instance in results:
    print(instance)

######################################################


# get traded futures pairs

print("traded futures pairs:")

results = (RoutingSession.session.query(Currencies.NseFuturesTimeSeries.SYMBOL, 
                                        func.min(Currencies.NseFuturesTimeSeries.TIME_STAMP).label('start_dt'), 
                                        func.max(Currencies.NseFuturesTimeSeries.TIME_STAMP).label('end_dt'))
            .group_by(Currencies.NseFuturesTimeSeries.SYMBOL)
            .order_by(text('start_dt'))
            .all())

for instance in results:
    print(instance)
    
# get the latest USDINR option chain for the nearest expiry    

print("latest USDINR option chain for the nearest expiry:")

end_dt = RoutingSession.session.query(func.max(Currencies.NseOptionsTimeSeries.TIME_STAMP)).scalar() 

expiry = (RoutingSession.session.query(func.min(Currencies.NseOptionsTimeSeries.EXPIRY))
          .filter(and_(Currencies.NseOptionsTimeSeries.SYMBOL == "USDINR",
                       Currencies.NseOptionsTimeSeries.TIME_STAMP == end_dt))
          .scalar())

results = (RoutingSession.session.query(Currencies.NseOptionsTimeSeries)
      .filter(and_(Currencies.NseOptionsTimeSeries.SYMBOL == "USDINR", 
                   Currencies.NseOptionsTimeSeries.EXPIRY == expiry,
                   Currencies.NseOptionsTimeSeries.TIME_STAMP == end_dt))
      .order_by(Currencies.NseOptionsTimeSeries.STRIKE, Currencies.NseOptionsTimeSeries.OTYPE)
      .all())

for instance in results:
    print(instance)
    
# get the currencies tracked by AlphaVantage end-of-day

print("AlphaVantage end-of-day pairs:")

results = (RoutingSession.session.query(Currencies.AvEodTimeSeries.SYMBOL, 
                                        func.min(Currencies.AvEodTimeSeries.TIME_STAMP).label('start_dt'), 
                                        func.max(Currencies.AvEodTimeSeries.TIME_STAMP).label('end_dt'))
            .group_by(Currencies.AvEodTimeSeries.SYMBOL)
            .order_by(text('start_dt'))
            .all())

for instance in results:
    print(instance)
    

# get the currencies tracked by AlphaVantage 30-min bars
    
print("AlphaVantage 30-min bars:")

results = (RoutingSession.session.query(Currencies.Av30minTimeSeries.SYMBOL, 
                                        func.min(Currencies.Av30minTimeSeries.TIME_STAMP).label('start_dt'), 
                                        func.max(Currencies.Av30minTimeSeries.TIME_STAMP).label('end_dt'),
                                        func.count(Currencies.Av30minTimeSeries.TIME_STAMP).label('count'))
            .group_by(Currencies.Av30minTimeSeries.SYMBOL)
            .order_by(text('count desc'))
            .all())

for instance in results:
    print(instance)            
    