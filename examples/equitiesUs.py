"""This example illustrates how to use the EquitiesUs data-set."""

import sys
sys.path.append("..")
    
from sqlalchemy import func, and_, or_
from plutoPy.model import RoutingSession, EquitiesUs
from datetime import date, datetime, timedelta

# last 10 days of AAPL stock prices
results = (RoutingSession.session.query(EquitiesUs.EodAdjustedTimeSeries)
           .filter(EquitiesUs.EodAdjustedTimeSeries.SYMBOL == 'AAPL')
           .order_by(EquitiesUs.EodAdjustedTimeSeries.TIME_STAMP.desc())
           .limit(10)
           .all())

print("last 10 days of AAPL stock prices:")
for instance in results:
    print(instance)


# biggest 20 listed stocks

results = (RoutingSession.session.query(EquitiesUs.Tickers)
            .order_by(EquitiesUs.Tickers.MKT_CAP.desc())
            .limit(20)
            .all())

print("biggest 20 listed stocks:")
for instance in results:
    print(instance)
    
# M&A in the last 90 days
    
startDt = date.today() - timedelta(days=90)
results = (RoutingSession.session.query(EquitiesUs.Tickers.SYMBOL, EquitiesUs.Tickers.NAME, 
                                        EquitiesUs.SecMeta.SIC_DESC, 
                                        EquitiesUs.SecFilings.FILING_DATE, EquitiesUs.SecFilings.FILING_TYPE)
           .join(EquitiesUs.Tickers, EquitiesUs.Tickers.SYMBOL == EquitiesUs.SecFilings.SYMBOL) 
           .join(EquitiesUs.SecMeta, EquitiesUs.SecMeta.SYMBOL == EquitiesUs.SecFilings.SYMBOL)
           .filter(and_(EquitiesUs.SecFilings.FILING_DATE >= startDt, 
                        or_(EquitiesUs.SecFilings.FILING_TYPE == 'DEFM14A', 
                            EquitiesUs.SecFilings.FILING_TYPE == 'SC14D9C')))
           .order_by(EquitiesUs.Tickers.MKT_CAP.desc())
           .all())

print("M&A in the last 90 days:")
for instance in results:
    print(instance)    
    
    
    