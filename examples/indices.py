"""This example illustrates how to get a list of all the latest NSE Indices, and
the constituents of a specific index."""

import sys
sys.path.append("..")
    
from sqlalchemy import func
from plutoPy.model import RoutingSession, Indices

# a list of all current NSE indices

end_dt = RoutingSession.session.query(func.max(Indices.NseTimeSeries.TIME_STAMP)).scalar()

results = (RoutingSession.session.query(Indices.NseTimeSeries.NAME)
            .filter(Indices.NseTimeSeries.TIME_STAMP == end_dt)
            .all())

print(f"fetched: {len(results)}")
for instance in results:
    print(instance.NAME)
    
# fetch the latest NSE NIFTY 50 constituents    
    
latest_dt = (RoutingSession.session.query(func.max(Indices.NseConstituents.TIME_STAMP))
            .filter(Indices.NseConstituents.NAME == "NIFTY 50")
            .scalar())    

results = (RoutingSession.session.query(Indices.NseConstituents.SYMBOL, Indices.NseConstituents.CAP_WEIGHT)
            .filter(Indices.NseConstituents.TIME_STAMP == latest_dt, Indices.NseConstituents.NAME == "NIFTY 50")
            .all())

print(f"fetched: {len(results)}")
for instance in results:
    print(instance)

# fetch the latest BSE SENSEX constituents    
    
latest_dt = (RoutingSession.session.query(func.max(Indices.BseConstituents.TIME_STAMP))
             .filter(Indices.BseConstituents.NAME == "sp bse sensex")
             .scalar())    

results = (RoutingSession.session.query(Indices.BseConstituents.SYMBOL, Indices.BseConstituents.SECURITY_NAME)
            .filter(Indices.BseConstituents.TIME_STAMP == latest_dt, Indices.BseConstituents.NAME == "sp bse sensex")
            .all())

print(f"fetched: {len(results)}")
for instance in results:
    print(instance)

