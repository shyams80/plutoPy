from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
import urllib.parse

from .Db import StockViz, StockVizUs, StockVizUs2, StockVizDyn, StockVizBeka

from ..Config import config
import plutoDbPy

dbNames = config['DEFAULT']['DB_NAMES'].split(",")
dbNames = [dn.strip() for dn in dbNames]

qpass = urllib.parse.quote_plus(config['DEFAULT']['REDIS_PASSWORD'])
redisSever = config['DEFAULT']['REDIS_SERVER']

engines = {}
for dbName in dbNames:
    conTemplate = config["CONNECTIONS"][dbName].replace("{XXX}", f":{qpass}@{redisSever}")
    engines[dbName] = create_engine(conTemplate, module = plutoDbPy.dbapi, echo=False)
      

class RoutingSession(Session):
    def get_bind(self, mapper=None, clause=None):
        if mapper and issubclass(mapper.class_, StockViz):
            return engines['StockViz']
        elif mapper and issubclass(mapper.class_, StockVizUs):
            return engines['StockVizUs']
        elif mapper and issubclass(mapper.class_, StockVizUs2):
            return engines['StockVizUs2']
        elif mapper and issubclass(mapper.class_, StockVizDyn):
            return engines['StockVizDyn']
        elif mapper and issubclass(mapper.class_, StockVizBeka):
            return engines['StockVizBeka']
        elif self._flushing:
            raise Exception("Unknown database!")
        
Session = sessionmaker(class_ = RoutingSession)
session = Session()        