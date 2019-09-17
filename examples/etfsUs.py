"""This example illustrates how to use the EtfsUs data-set."""

import sys
sys.path.append("..")
    
from sqlalchemy import func, and_, or_
from plutoPy.model import RoutingSession, ETFsUs
from datetime import date, datetime, timedelta

# biggest 20 ETFs

results = (RoutingSession.session.query(ETFsUs.Meta)
            .order_by(ETFsUs.Meta.AUM.desc())
            .limit(20)
            .all())

print("biggest 20 ETFs:")
for instance in results:
    print(instance)
    
# oldest 20 ETFs

results = (RoutingSession.session.query(ETFsUs.Meta)
            .order_by(ETFsUs.Meta.LAUNCH_DATE)
            .limit(20)
            .all())

print("oldest 20 ETFs:")
for instance in results:
    print(instance)    