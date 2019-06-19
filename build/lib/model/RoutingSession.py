from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

import pypyodbc
from .Db import StockViz, StockVizUs, StockVizUs2

from Config import config

engines = {
    'stockviz': create_engine(config['DEFAULT']['NORWAY_STOCKVIZ_CON'], module=pypyodbc, echo=True),
    'stockvizUs': create_engine(config['DEFAULT']['NORWAY_STOCKVIZ_US_CON'], module=pypyodbc, echo=True),
    'stockvizUs2': create_engine(config['DEFAULT']['NORWAY_STOCKVIZ_US2_CON'], module=pypyodbc, echo=True)
}

class RoutingSession(Session):
    def get_bind(self, mapper=None, clause=None):
        if mapper and issubclass(mapper.class_, StockViz):
            return engines['stockviz']
        elif mapper and issubclass(mapper.class_, StockVizUs):
            return engines['stockvizUs']
        elif mapper and issubclass(mapper.class_, StockVizUs2):
            return engines['stockvizUs2']
        elif self._flushing:
            raise Exception("Unknown database!")
        
Session = sessionmaker(class_ = RoutingSession)
session = Session()        