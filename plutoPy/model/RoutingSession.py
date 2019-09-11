from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
import urllib.parse
from pydoc import locate

from .Db import StockViz, StockVizUs, StockVizUs2, StockVizDyn, StockVizBeka

from ..Config import config
import plutoDbPy

dbNames = config['DEFAULT']['DB_NAMES'].split(",")
dbNames = [dn.strip() for dn in dbNames]

engines = {}
for dbName in dbNames:
    engines[dbName] = create_engine(config["CONNECTIONS"][dbName], module = plutoDbPy.dbapi, echo=False)
      

class RoutingSession(Session):
    def get_bind(self, mapper=None, clause=None):
        for dbName in dbNames:
            if mapper and issubclass(mapper.class_, locate("plutoPy.model.Db." + dbName)):
                return engines[dbName]
            
        if self._flushing:
            raise Exception("Unknown database!")
        
Session = sessionmaker(class_ = RoutingSession)
session = Session()        