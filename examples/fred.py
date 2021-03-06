"""This example illustrates how to get a list of all Fred time-series that have 'India' in its title."""

import sys
sys.path.append("..")
    
from sqlalchemy import func
from plutoPy.model import RoutingSession, Fred

#a list of india focused indices mainted by the Fred
results = RoutingSession.session.query(Fred.Meta.SERIES_ID, Fred.Meta.TICKER, Fred.Meta.NAME, func.min(Fred.TimeSeries.TIME_STAMP).label("start_dt"), func.max(Fred.TimeSeries.TIME_STAMP).label("end_dt")).\
                        join(Fred.TimeSeries, Fred.Meta.SERIES_ID == Fred.TimeSeries.SERIES_ID).\
                        filter(Fred.Meta.NAME.ilike('%india %')).\
                        group_by(Fred.Meta.SERIES_ID, Fred.Meta.TICKER, Fred.Meta.NAME).all()

print(f"fetched: {len(results)}")
for instance in results:
    print(instance)