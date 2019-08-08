"""This example illustrates how to use the Fama-French dataset."""

import sys
sys.path.append("..")
    
from sqlalchemy import func, text
from plutoPy.model import RoutingSession, FamaFrench

# show data-ranges for Fama-french factors

results = (RoutingSession.session.query(FamaFrench.FiveFactor3x2Daily.KEY_ID, 
                                        func.min(FamaFrench.FiveFactor3x2Daily.TIME_STAMP).label("start_dt"), 
                                        func.max(FamaFrench.FiveFactor3x2Daily.TIME_STAMP).label("end_dt"))
            .group_by(FamaFrench.FiveFactor3x2Daily.KEY_ID)
            .all())

print(f"fetched: {len(results)}")
for instance in results:
    print(instance)

# show data-ranges for Fama-french industry daily returns

results = (RoutingSession.session.query(FamaFrench.Industry49Daily.KEY_ID,
                                        FamaFrench.Industry49Daily.RET_TYPE, 
                                        func.min(FamaFrench.Industry49Daily.TIME_STAMP).label("start_dt"), 
                                        func.max(FamaFrench.Industry49Daily.TIME_STAMP).label("end_dt"))
            .group_by(FamaFrench.Industry49Daily.KEY_ID, FamaFrench.Industry49Daily.RET_TYPE)
            .order_by(text("start_dt"))
            .all())

print(f"fetched: {len(results)}")
for instance in results:
    print(instance)
    
# show data-ranges for Fama-french momentum daily returns

results = (RoutingSession.session.query(FamaFrench.MomentumDaily.KEY_ID, 
                                        FamaFrench.MomentumDaily.RET_TYPE,
                                        func.min(FamaFrench.MomentumDaily.TIME_STAMP).label("start_dt"), 
                                        func.max(FamaFrench.MomentumDaily.TIME_STAMP).label("end_dt"))
            .group_by(FamaFrench.MomentumDaily.KEY_ID, FamaFrench.MomentumDaily.RET_TYPE)
            .order_by(text("start_dt"))
            .all())

print(f"fetched: {len(results)}")
for instance in results:
    print(instance)  
    
    
# show data-ranges for Fama-french momentum daily returns

results = (RoutingSession.session.query(FamaFrench.MomentumMonthly.KEY_ID, 
                                        FamaFrench.MomentumMonthly.RET_TYPE,
                                        func.min(FamaFrench.MomentumMonthly.TIME_STAMP).label("start_dt"), 
                                        func.max(FamaFrench.MomentumMonthly.TIME_STAMP).label("end_dt"))
            .group_by(FamaFrench.MomentumMonthly.KEY_ID, FamaFrench.MomentumMonthly.RET_TYPE)
            .order_by(text("start_dt"))
            .all())

print(f"fetched: {len(results)}")
for instance in results:
    print(instance)   