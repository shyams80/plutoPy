"""This example illustrates how to use the MutualFundsIndia data-set"""

import sys
sys.path.append("..")

import pandas as pd
from sqlalchemy import func, or_, and_
from plutoPy.model import RoutingSession, MutualFundsIndia

# who are the biggest 5?

lastAumDate = RoutingSession.session.query(func.max(MutualFundsIndia.AumFundwise.PERIOD)).scalar()
print(f"{lastAumDate}")

aums = (RoutingSession.session.query(MutualFundsIndia.AumFundwise.FUND, MutualFundsIndia.AumFundwise.AVG_AUM_WO_FOFD + MutualFundsIndia.AumFundwise.AVG_AUM_FOFD)
        .filter(MutualFundsIndia.AumFundwise.PERIOD == lastAumDate)
        .order_by((MutualFundsIndia.AumFundwise.AVG_AUM_WO_FOFD + MutualFundsIndia.AumFundwise.AVG_AUM_FOFD).desc())).all()

aumDf = pd.DataFrame(aums, columns=['FUND', 'AUM']) #analyze this!
print(aumDf[0:5])

# deep dive: largest 10 mid-cap funds by AUM

lastMetaDate = RoutingSession.session.query(func.max(MutualFundsIndia.Meta.AS_OF)).scalar()
lastSwDate = RoutingSession.session.query(func.max(MutualFundsIndia.AumSchemewise.PERIOD)).scalar()
print(f"{lastMetaDate}/{lastSwDate}")

# Meta to filter for the 'Mid-Cap' category
# AumSchemewise to sort funds by AUM - largest first
# NavTimeSeries to get the start and end dates for which NAVs are available

midCaps = (RoutingSession.session.query(MutualFundsIndia.Meta.SCHEME_CODE, 
                                       MutualFundsIndia.AumSchemewise.SCHEME_NAME,
                                       MutualFundsIndia.Meta.CATEGORY, 
                                       MutualFundsIndia.AumSchemewise.AVG_AUM_WO_FOFD,
                                       func.min(MutualFundsIndia.NavTimeSeries.TIME_STAMP).label("start_dt"), 
                                       func.max(MutualFundsIndia.NavTimeSeries.TIME_STAMP).label("end_dt"))
        .join(MutualFundsIndia.AumSchemewise, MutualFundsIndia.Meta.SCHEME_CODE == MutualFundsIndia.AumSchemewise.SCHEME_CODE)
        .join(MutualFundsIndia.NavTimeSeries, MutualFundsIndia.NavTimeSeries.SCHEME_CODE == MutualFundsIndia.AumSchemewise.SCHEME_CODE)
        .filter(and_(MutualFundsIndia.AumSchemewise.PERIOD == lastSwDate,
                    MutualFundsIndia.Meta.AS_OF == lastMetaDate, 
                    MutualFundsIndia.Meta.CATEGORY == 'Mid-Cap'))
        .group_by(MutualFundsIndia.Meta.SCHEME_CODE, 
            MutualFundsIndia.AumSchemewise.SCHEME_NAME,
            MutualFundsIndia.Meta.CATEGORY, 
            MutualFundsIndia.AumSchemewise.AVG_AUM_WO_FOFD)
        .order_by(MutualFundsIndia.AumSchemewise.AVG_AUM_WO_FOFD.desc())).all()

print(f"fetched: {len(midCaps)}")

# get a pandas dataframe out of the list of tuples
mcDf = pd.DataFrame(midCaps)

pd.set_option('display.max_columns', None)
print(mcDf[0:10])

# get the NAV time-series
scode = int(mcDf.iloc[2]['SCHEME_CODE'])
navs = (RoutingSession.session.query(MutualFundsIndia.NavTimeSeries.TIME_STAMP, MutualFundsIndia.NavTimeSeries.NAV)
        .filter(MutualFundsIndia.NavTimeSeries.SCHEME_CODE == scode)
        .order_by(MutualFundsIndia.NavTimeSeries.TIME_STAMP)).all()

navDf = pd.DataFrame(navs) #analyze this!
print(navDf[0:10])         