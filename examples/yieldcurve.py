import sys
sys.path.append("..")
    
from sqlalchemy import func, and_
from sqlalchemy.orm import aliased
from plutoPy.model import RoutingSession, YieldCurve

#fetch the latest India Zero Coupon Bond yields

end_dt = RoutingSession.session.query(func.max(YieldCurve.IndiaZeroCoupon.TIME_STAMP)).scalar()

curve = (RoutingSession.session.query(YieldCurve.IndiaZeroCoupon)
         .filter(YieldCurve.IndiaZeroCoupon.TIME_STAMP == end_dt)
         .order_by(YieldCurve.IndiaZeroCoupon.MATURITY)
         .all())

print("the latest India Zero Coupon Bond yields")
for c in curve:
    print(c)
    
#fetch the latest US Treasury Yield Curve    

end_dt = RoutingSession.session.query(func.max(YieldCurve.UsTreasury.TIME_STAMP)).scalar()

curve = (RoutingSession.session.query(YieldCurve.UsTreasury)
         .filter(YieldCurve.UsTreasury.TIME_STAMP == end_dt)
         .all())

print("the latest US Treasury Yield Curve")
for c in curve:
    print(c)
    
#fetch the latest Euro area yield curve

end_dt = RoutingSession.session.query(func.max(YieldCurve.EuroArea.TIME_STAMP)).scalar()

alias1 = aliased(YieldCurve.EuroArea)
alias2 = aliased(YieldCurve.EuroArea)

curve = (RoutingSession.session.query(alias1.TENOR_Y, alias1.TENOR_M, alias1.VALUE.label('G_N_A'), alias2.VALUE.label('G_N_C'))
         .join(alias2, and_(alias1.TENOR_Y == alias2.TENOR_Y, alias1.TENOR_M == alias2.TENOR_M, alias1.TIME_STAMP == alias2.TIME_STAMP))
         .filter(and_(alias1.TIME_STAMP == end_dt, alias1.CURVE_ID == 'G_N_A', alias2.CURVE_ID == 'G_N_C'))
         .order_by(alias1.TENOR_Y, alias1.TENOR_M)
         .all())

print("the latest Euro Area Yield Curve")
for c in curve:
    print(c)    