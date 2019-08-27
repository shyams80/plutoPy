"""This example illustrates how to use the International Monetary Fund data-set"""

import sys
sys.path.append("..")
    
from sqlalchemy import func, and_
from plutoPy.model import RoutingSession, InternationalMonetaryFund
from sqlalchemy.orm import aliased

Meta = aliased(InternationalMonetaryFund.Meta)
TimeSeries = aliased(InternationalMonetaryFund.TimeSeries)

# get meta-data about monthly indicators pertaining to India currently maintained

results = (RoutingSession.session.query(Meta)
            .filter(and_(Meta.AREA == "India", Meta.END_YEAR == 2019, Meta.FREQ == 'M'))
            .all())
           
print(f"fetched: {len(results)}")
for instance in results:
    print(instance)
    
# get Indian IIP index (-2147472396)   

results = (RoutingSession.session.query(TimeSeries)
            .filter(TimeSeries.ID == -2147472396)
            .order_by(TimeSeries.YEAR, TimeSeries.MONTH)
            .all())
           
print(f"fetched: {len(results)}")
for instance in results:
    print(instance)
    