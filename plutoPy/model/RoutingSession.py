from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
import urllib.parse
from pydoc import locate
from psycopg2.pool import ThreadedConnectionPool

from .Db import StockViz, StockVizUs, StockVizUs2, StockVizDyn, StockVizBeka

from ..Config import config
import plutoDbPy

dbNamesOdbc = [dn.strip() for dn in config['DEFAULT']['ODBC_DB_NAMES'].split(",")]
dbNamesPg = [dn.strip() for dn in config['DEFAULT']['PG_DB_NAMES'].split(",")]

dbNames = dbNamesOdbc + dbNamesPg

engines = {}
for dbName in dbNamesOdbc:
    engines[dbName] = create_engine(config["CONNECTIONS"][dbName], module = plutoDbPy.dbapiOdbc, echo=False)
    
for dbName in dbNamesPg:
    engines[dbName] = create_engine(config["CONNECTIONS"][dbName], module = plutoDbPy.dbapiPg, echo=False)
    
class RoutingSession(Session):
    def get_bind(self, mapper=None, clause=None):
        for dbName in dbNames:
            if mapper and issubclass(mapper.class_, locate("plutoPy.model.Db." + dbName)):
                return engines[dbName]
            
        if self._flushing:
            raise Exception("Unknown database!")
        
Session = sessionmaker(class_ = RoutingSession)
session = Session()        