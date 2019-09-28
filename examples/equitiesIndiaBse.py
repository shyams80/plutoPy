"""This example illustrates how to use the EquitiesIndiaBse data-set."""

import sys
sys.path.append("..")
    
from sqlalchemy import func, and_, or_, text
from plutoPy.model import RoutingSession, EquitiesIndiaBse
from datetime import date, datetime

symbol = "SBIN"

#get BSE's code for a symbol

secInfo = (RoutingSession.session.query(EquitiesIndiaBse.Tickers)
           .filter(EquitiesIndiaBse.Tickers.SYMBOL == symbol)
           .all())

print(secInfo)

code = secInfo[0].CODE

# fetch some "misc" info

end_dt = RoutingSession.session.query(func.max(EquitiesIndiaBse.MiscInfo.TIME_STAMP)).scalar() 

results = (RoutingSession.session.query(EquitiesIndiaBse.MiscInfo)
            .filter(and_(EquitiesIndiaBse.MiscInfo.TIME_STAMP == end_dt, EquitiesIndiaBse.MiscInfo.CODE == code))
            .all())

print("misc info:")
for instance in results:
    print(instance)
    
# fetch the latest end-of-day prices

end_dt = RoutingSession.session.query(func.max(EquitiesIndiaBse.EodTimeSeries.TIME_STAMP)).scalar()

results = (RoutingSession.session.query(EquitiesIndiaBse.EodTimeSeries)
            .filter(and_(EquitiesIndiaBse.EodTimeSeries.TIME_STAMP == end_dt, EquitiesIndiaBse.EodTimeSeries.CODE == code))
            .all())

print(f"fetched: {len(results)}")
for instance in results:
    print(instance)    
    
# fetch the last 10 day EOD prices for State Bank of India

results = (RoutingSession.session.query(EquitiesIndiaBse.EodTimeSeries)
            .filter(EquitiesIndiaBse.EodTimeSeries.CODE == code)
            .order_by(EquitiesIndiaBse.EodTimeSeries.TIME_STAMP.desc())
            .limit(10)
            .all())

print("last 10 day EOD prices:")
for instance in results:
    print(instance)    
        
        
# fetch the last 24 quarter EPS for State Bank of India

results = (RoutingSession.session.query(EquitiesIndiaBse.CorporateResults)
            .filter(and_(EquitiesIndiaBse.CorporateResults.CODE == code, 
                         EquitiesIndiaBse.CorporateResults.KEY.ilike('%diluted%'),
                         EquitiesIndiaBse.CorporateResults.KEY.ilike('%after%'),
                         func.datediff(text('day'), EquitiesIndiaBse.CorporateResults.PERIOD_BEGIN, EquitiesIndiaBse.CorporateResults.PERIOD_END) < 100))
            .order_by(EquitiesIndiaBse.CorporateResults.PERIOD_END.desc())
            .limit(24)
            .all())

print("the last 24 quarter EPS: ")  
for instance in results:
    print(instance)         