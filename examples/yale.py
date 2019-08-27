"""This example illustrates how to use the Yale/Shiller dataset."""

import sys
sys.path.append("..")
    
from sqlalchemy import func, text, extract
from plutoPy.model import RoutingSession, Yale
from datetime import date

# start and end dates of confidence indices

results = (RoutingSession.session.query(Yale.Confidence.NAME,
                                        func.min(Yale.Confidence.TIME_STAMP).label("start_dt"),
                                        func.max(Yale.Confidence.TIME_STAMP).label("end_dt"))
            .group_by(Yale.Confidence.NAME)
            .all())

print(f"fetched: {len(results)}")
for instance in results:
    print(instance)
    
# SP500 close and CAPE at the end of each year since 1995

startDate = date(1995, 12, 1)    
results = (RoutingSession.session.query(extract('year', Yale.SP500.TIME_STAMP).label('Y'), Yale.SP500.CLOSE, Yale.SP500.CAPE)
           .filter(extract('month', Yale.SP500.TIME_STAMP) == 12 and Yale.SP500.TIME_STAMP >= startDate)
           .order_by(Yale.SP500.TIME_STAMP)
           .all())

print(f"fetched: {len(results)}")
for instance in results:
    print(instance)
