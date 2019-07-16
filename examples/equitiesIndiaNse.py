"""This example illustrates how to use the EquitiesIndiaNse data-set."""

import sys
sys.path.append("..")
    
from sqlalchemy import func, and_, or_
from plutoPy.model import RoutingSession, EquitiesIndiaNse
from datetime import date, datetime

# fetch the earliest 10 listed equity

results = (RoutingSession.session.query(EquitiesIndiaNse.Tickers)
           .order_by(EquitiesIndiaNse.Tickers.DATE_LISTING)
           .limit(10)
           .all())

for instance in results:
    print(instance)
    
# fetch some "misc" info for State Bank of India   

end_dt = RoutingSession.session.query(func.max(EquitiesIndiaNse.MiscInfo.TIME_STAMP)).scalar() 

results = (RoutingSession.session.query(EquitiesIndiaNse.MiscInfo)
            .filter(and_(EquitiesIndiaNse.MiscInfo.TIME_STAMP == end_dt, EquitiesIndiaNse.MiscInfo.SYMBOL == 'SBIN'))
            .all())

print("misc info for SBIN:")
for instance in results:
    print(instance)

# fetch the market-cap decile of DHFL since we started capturing the data-set

results = (RoutingSession.session.query(EquitiesIndiaNse.MarketCapDecile)
            .filter(EquitiesIndiaNse.MarketCapDecile.SYMBOL == 'DHFL')
            .all())

print("market-cap deciles for DHFL over time:")
for instance in results:
    print(instance)
    
# fetch the latest end-of-day prices for State Bank of India

end_dt = RoutingSession.session.query(func.max(EquitiesIndiaNse.EodTimeSeries.TIME_STAMP)).scalar()

results = (RoutingSession.session.query(EquitiesIndiaNse.EodTimeSeries)
            .filter(and_(EquitiesIndiaNse.EodTimeSeries.TIME_STAMP == end_dt, EquitiesIndiaNse.EodTimeSeries.SYMBOL == 'SBIN'))
            .all())

print(f"fetched: {len(results)}")
for instance in results:
    print(instance)
    
# fetch the last 10 day EOD prices for State Bank of India

results = (RoutingSession.session.query(EquitiesIndiaNse.EodTimeSeries)
            .filter(and_(or_(EquitiesIndiaNse.EodTimeSeries.SERIES == 'EQ', EquitiesIndiaNse.EodTimeSeries.SERIES == 'BE'), 
                         EquitiesIndiaNse.EodTimeSeries.SYMBOL == 'SBIN'))
            .order_by(EquitiesIndiaNse.EodTimeSeries.TIME_STAMP.desc())
            .limit(10)
            .all())

for instance in results:
    print(instance)    
    
    
# UPL did a 1:2 bonus on 2019-07-02. see unadjusted eod vs. adjusted eod

startDt = datetime(2019, 6, 15)    
endDt = datetime(2019, 7, 15)

print("unadjusted eod")
results = (RoutingSession.session.query(EquitiesIndiaNse.EodTimeSeries)
            .filter(and_(or_(EquitiesIndiaNse.EodTimeSeries.SERIES == 'EQ', EquitiesIndiaNse.EodTimeSeries.SERIES == 'BE'), 
                         EquitiesIndiaNse.EodTimeSeries.SYMBOL == 'UPL',
                         EquitiesIndiaNse.EodTimeSeries.TIME_STAMP >= startDt,
                         EquitiesIndiaNse.EodTimeSeries.TIME_STAMP <= endDt))
            .order_by(EquitiesIndiaNse.EodTimeSeries.TIME_STAMP)
            .all())

for instance in results:
    print(instance)

print("adjusted eod")    
results = (RoutingSession.session.query(EquitiesIndiaNse.EodAdjustedTimeSeries)
            .filter(and_(EquitiesIndiaNse.EodAdjustedTimeSeries.SYMBOL == 'UPL',
                         EquitiesIndiaNse.EodAdjustedTimeSeries.TIME_STAMP >= startDt,
                         EquitiesIndiaNse.EodAdjustedTimeSeries.TIME_STAMP <= endDt))
            .order_by(EquitiesIndiaNse.EodAdjustedTimeSeries.TIME_STAMP)
            .all())

for instance in results:
    print(instance)            

 
# fetch the last 10 day returns for State Bank of India

results = (RoutingSession.session.query(EquitiesIndiaNse.DailyReturns)
            .filter(EquitiesIndiaNse.DailyReturns.SYMBOL == 'SBIN')
            .order_by(EquitiesIndiaNse.DailyReturns.TIME_STAMP.desc())
            .limit(10)
            .all())

for instance in results:
    print(instance)        
    
# fetch the last 10 corporate actions for State Bank of India

results = (RoutingSession.session.query(EquitiesIndiaNse.CorporateActions)
            .filter(EquitiesIndiaNse.CorporateActions.SYMBOL == 'SBIN')
            .order_by(EquitiesIndiaNse.CorporateActions.EX_DATE.desc())
            .limit(10)
            .all())

for instance in results:
    print(instance)
    
    
# fetch the last 24 quarter EPS for State Bank of India

refIds = (RoutingSession.session.query(EquitiesIndiaNse.CorporateResultsMeta)
            .filter(and_(EquitiesIndiaNse.CorporateResultsMeta.SYMBOL == 'SBIN'),
                    EquitiesIndiaNse.CorporateResultsMeta.IS_CONSOLIDATED == False,
                    EquitiesIndiaNse.CorporateResultsMeta.PERIOD.ilike('%quarter'))
            .order_by(EquitiesIndiaNse.CorporateResultsMeta.PERIOD_END.desc())
            .limit(24)
            .all())

for instance in refIds:
    print(instance)
    
    results = (RoutingSession.session.query(EquitiesIndiaNse.CorporateResults)
               .filter(and_(EquitiesIndiaNse.CorporateResults.REF_ID == instance.REF_ID,
                            EquitiesIndiaNse.CorporateResults.KEY.ilike('%diluted%before%')))
               .all())
    
    for r in results:
        print(r)
        

