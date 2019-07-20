"""This example illustrates how to use the EquitiesFuturesAndOptionsIndiaNse data-set."""

import sys
sys.path.append("..")

import pandas as pd    
from sqlalchemy import func, and_, or_, text, Integer
from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import cast
from plutoPy.model import RoutingSession, EquitiesFuturesAndOptionsIndiaNse
from datetime import date, datetime, timedelta

# get all NIFTY futures contract traded right now

print("NIFTY futures contract traded right now")

end_dt = RoutingSession.session.query(func.max(EquitiesFuturesAndOptionsIndiaNse.FuturesEodTimeSeries.TIME_STAMP)).scalar() 

results = (RoutingSession.session.query(EquitiesFuturesAndOptionsIndiaNse.FuturesEodTimeSeries)
      .filter(and_(EquitiesFuturesAndOptionsIndiaNse.FuturesEodTimeSeries.SYMBOL == "NIFTY", 
                   EquitiesFuturesAndOptionsIndiaNse.FuturesEodTimeSeries.TIME_STAMP == end_dt))
      .all())

for instance in results:
    print(instance)
    
# get all NIFTY option contracts at the nearest expiry traded right now

print("NIFTY option contracts at the nearest expiry traded right now")

end_dt = RoutingSession.session.query(func.max(EquitiesFuturesAndOptionsIndiaNse.OptionsEodTimeSeries.TIME_STAMP)).scalar() 

expiry = (RoutingSession.session.query(func.min(EquitiesFuturesAndOptionsIndiaNse.OptionsEodTimeSeries.EXPIRY))
          .filter(and_(EquitiesFuturesAndOptionsIndiaNse.OptionsEodTimeSeries.SYMBOL == "NIFTY",
                       EquitiesFuturesAndOptionsIndiaNse.OptionsEodTimeSeries.TIME_STAMP == end_dt))
          .scalar())

results = (RoutingSession.session.query(EquitiesFuturesAndOptionsIndiaNse.OptionsEodTimeSeries)
      .filter(and_(EquitiesFuturesAndOptionsIndiaNse.OptionsEodTimeSeries.SYMBOL == "NIFTY", 
                   EquitiesFuturesAndOptionsIndiaNse.OptionsEodTimeSeries.EXPIRY == expiry,
                   cast(EquitiesFuturesAndOptionsIndiaNse.OptionsEodTimeSeries.STRIKE, Integer) % 100 == 0,
                   EquitiesFuturesAndOptionsIndiaNse.OptionsEodTimeSeries.TIME_STAMP == end_dt))
      .order_by(EquitiesFuturesAndOptionsIndiaNse.OptionsEodTimeSeries.STRIKE, EquitiesFuturesAndOptionsIndiaNse.OptionsEodTimeSeries.OTYPE)
      .all())

# get all greeks for the NIFTY option contracts at the nearest expiry traded right now

print("greeks for the NIFTY option contracts at the nearest expiry traded right now")

end_dt = RoutingSession.session.query(func.max(EquitiesFuturesAndOptionsIndiaNse.OptionGreeks.TIME_STAMP)).scalar() 

expiry = (RoutingSession.session.query(func.min(EquitiesFuturesAndOptionsIndiaNse.OptionGreeks.EXPIRY))
          .filter(and_(EquitiesFuturesAndOptionsIndiaNse.OptionGreeks.SYMBOL == "NIFTY",
                       EquitiesFuturesAndOptionsIndiaNse.OptionGreeks.TIME_STAMP == end_dt))
          .scalar())

results = (RoutingSession.session.query(EquitiesFuturesAndOptionsIndiaNse.OptionGreeks)
      .filter(and_(EquitiesFuturesAndOptionsIndiaNse.OptionGreeks.SYMBOL == "NIFTY", 
                   EquitiesFuturesAndOptionsIndiaNse.OptionGreeks.EXPIRY == expiry,
                   cast(EquitiesFuturesAndOptionsIndiaNse.OptionGreeks.STRIKE, Integer) % 100 == 0,
                   EquitiesFuturesAndOptionsIndiaNse.OptionGreeks.TIME_STAMP == end_dt))
      .order_by(EquitiesFuturesAndOptionsIndiaNse.OptionGreeks.STRIKE, EquitiesFuturesAndOptionsIndiaNse.OptionGreeks.OTYPE)
      .all())


for instance in results:
    print(instance)    
    
# get NIFTY's lot-sizes at different expiries

print("NIFTY's lot-sizes at different expiries")

futureDate = date.today() + timedelta(days=30*3)

results = (RoutingSession.session.query(EquitiesFuturesAndOptionsIndiaNse.LotSize)
      .filter(and_(EquitiesFuturesAndOptionsIndiaNse.LotSize.SYMBOL == "NIFTY", EquitiesFuturesAndOptionsIndiaNse.LotSize.CONTRACT <= futureDate))
      .order_by(EquitiesFuturesAndOptionsIndiaNse.LotSize.CONTRACT.desc())
      .limit(10)
      .all())

for instance in results:
    print(instance)