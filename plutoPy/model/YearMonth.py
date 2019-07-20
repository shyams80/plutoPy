import sqlalchemy.types as types
from datetime import date, datetime
from collections import namedtuple

class YearMonth(namedtuple('YearMonth', ['month', 'year'])):
    __slots__ = ()
        
    def __str__(self):
        return f"{self.year}-{self.month}"

class YearMonthType(types.TypeDecorator):
    impl = types.Date
    
    def process_bind_param(self, value, dialect):
        # way in. value should be a YearMonth. returns date
        return date(value.year, value.month, 1)
    
    def process_result_value(self, value, dialect):
        # way out. value should be an date. returns YearMonth
        return YearMonth(year = value.year, month = value.month)
    