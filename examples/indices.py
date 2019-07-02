"""This example illustrates how to get a list of all the latest NSE Indices"""

import sys
sys.path.append("..")
    
from sqlalchemy import func
from plutoPy.model import RoutingSession, Indices

#a list of all current NSE indices
end_dt = RoutingSession.session.query(func.max(Indices.NseTimeSeries.TIME_STAMP)).scalar()

results = RoutingSession.session.query(Indices.NseTimeSeries.NAME).\
            filter(Indices.NseTimeSeries.TIME_STAMP == end_dt).all()

print(f"fetched: {len(results)}")
for instance in results:
    print(instance.NAME)