"""This example illustrates how to get a list of all NASDAQOMX TR Indices and their time-series"""

import sys
sys.path.append("..")
    
from sqlalchemy import func
from plutoPy.model import RoutingSession, NasdaqOmx

# fetch all "India" TR NASDAQOMX indices

results = (RoutingSession.session.query(NasdaqOmx.Meta.NAME,
                                       func.min(NasdaqOmx.TimeSeries.TIME_STAMP).label("start_dt"),
                                       func.max(NasdaqOmx.TimeSeries.TIME_STAMP).label("end_dt"))
            .join(NasdaqOmx.TimeSeries, NasdaqOmx.Meta.ID == NasdaqOmx.TimeSeries.ID)
            .filter(NasdaqOmx.Meta.NAME.ilike('% india %'))
            .group_by(NasdaqOmx.Meta.NAME).all())

print(f"fetched: {len(results)}")
for instance in results:
    print(instance)
