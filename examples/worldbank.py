"""This example illustrates how to use the World Bank data-set"""

import sys
sys.path.append("..")
    
from sqlalchemy import func, and_
from plutoPy.model import RoutingSession, WorldBank

#fetch all India related meta data

results = (RoutingSession.session.query(WorldBank.Meta)
           .filter(WorldBank.Meta.COUNTRY_NAME == "India")).all()
           
print(f"fetched: {len(results)}")
for instance in results:
    print(instance)
    
#fetch cpi inflation for India

results = (RoutingSession.session.query(WorldBank.TimeSeries)
           .filter(and_(WorldBank.TimeSeries.COUNTRY_KEY == 135, WorldBank.TimeSeries.INDICATOR_KEY == 6))
           .order_by(WorldBank.TimeSeries.YEAR)).all()
           
print(f"fetched: {len(results)}")
for instance in results:
    print(instance)
