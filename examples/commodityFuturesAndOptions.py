"""This example illustrates how to use the CommodityFuturesAndOptions data-set."""

import sys
sys.path.append("..")

import pandas as pd    
from sqlalchemy import func, and_, or_, text
from sqlalchemy.orm import aliased
from plutoPy.model import RoutingSession, CommodityFuturesAndOptions
from datetime import date, datetime

pd.set_option('display.max_columns', 500)

# get all the commodities that are being traded in COMEX and NYMEX

print("commodity futures that are being traded in COMEX and NYMEX")

end_dt = RoutingSession.session.query(func.max(CommodityFuturesAndOptions.CmeEod.TIME_STAMP)).scalar() 

alias1 = aliased(CommodityFuturesAndOptions.CmeEod)
alias2 = aliased(CommodityFuturesAndOptions.CmeEod)

t1 = (RoutingSession.session.query(alias1.PRODUCT_SYMBOL, alias1.PRODUCT_DESCRIPTION, func.sum(alias1.VOLUME).label("total_volume"))
      .filter(alias1.TIME_STAMP == end_dt)
      .group_by(alias1.PRODUCT_SYMBOL, alias1.PRODUCT_DESCRIPTION)
      .order_by(text("total_volume desc"))
      .all())

t2 = (RoutingSession.session.query(alias1.PRODUCT_SYMBOL, func.min(alias1.TIME_STAMP).label("start_dt"))
      .group_by(alias1.PRODUCT_SYMBOL)
      .order_by(text("start_dt"))
      .all())

pd1 = pd.DataFrame(t1, columns=['SYMBOL', 'DESCRIPTION', 'VOLUME'])
pd2 = pd.DataFrame(t2, columns=['SYMBOL', 'LISTED_DATE'])
tradedContracts = pd.merge(pd1, pd2, on='SYMBOL')

print(tradedContracts[tradedContracts['VOLUME'] > 0])
    
# get all the commodity futures that are being traded in MCX

print("commodity futures that are being traded in MCX")

end_dt = RoutingSession.session.query(func.max(CommodityFuturesAndOptions.McxEod.TIME_STAMP)).scalar() 

alias1 = aliased(CommodityFuturesAndOptions.McxEod)
alias2 = aliased(CommodityFuturesAndOptions.McxEod)

t1 = (RoutingSession.session.query(alias1.CONTRACT, func.sum(alias1.OI).label("total_oi"))
      .filter(and_(alias1.TIME_STAMP == end_dt, 
                   or_(alias1.OTYPE == 'XX', alias1.OTYPE == 'FUTCOM')))
      .group_by(alias1.CONTRACT)
      .order_by(text("total_oi desc"))
      .all())

t2 = (RoutingSession.session.query(alias1.CONTRACT, func.min(alias1.TIME_STAMP).label("start_dt"))
      .group_by(alias1.CONTRACT)
      .filter(or_(alias1.OTYPE == 'XX', alias1.OTYPE == 'FUTCOM'))
      .order_by(text("start_dt"))
      .all())

pd1 = pd.DataFrame(t1, columns=['SYMBOL', 'OI'])
pd2 = pd.DataFrame(t2, columns=['SYMBOL', 'LISTED_DATE'])
tradedContracts = pd.merge(pd1, pd2, on='SYMBOL')

print(tradedContracts[tradedContracts['OI'] > 0])

# get all the commodity futures that are being traded in MCX

print("commodity futures that are being traded in NCDEX")

end_dt = RoutingSession.session.query(func.max(CommodityFuturesAndOptions.NcdexEod.TIME_STAMP)).scalar() 

alias1 = aliased(CommodityFuturesAndOptions.NcdexEod)
alias2 = aliased(CommodityFuturesAndOptions.NcdexEod)

t1 = (RoutingSession.session.query(alias1.COMMODITY, func.sum(alias1.OI).label("total_oi"))
      .filter(alias1.TIME_STAMP == end_dt)
      .group_by(alias1.COMMODITY)
      .order_by(text("total_oi desc"))
      .all())

t2 = (RoutingSession.session.query(alias1.COMMODITY, func.min(alias1.TIME_STAMP).label("start_dt"))
      .group_by(alias1.COMMODITY)
      .order_by(text("start_dt"))
      .all())

pd1 = pd.DataFrame(t1, columns=['COMMODITY', 'OI'])
pd2 = pd.DataFrame(t2, columns=['COMMODITY', 'LISTED_DATE'])
tradedContracts = pd.merge(pd1, pd2, on='COMMODITY')

print(tradedContracts[tradedContracts['OI'] > 0])

