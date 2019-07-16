import sqlalchemy.types as types
from datetime import date, datetime

class IntegerDate(types.TypeDecorator):
    impl = types.Integer
    
    def process_bind_param(self, value, dialect):
        # way in. value should be a date. returns int
        return int(value.strftime('%Y%m%d'))
    
    def process_result_value(self, value, dialect):
        # way out. value should be an int. returns date
        return datetime.strptime(str(value), '%Y%m%d')
    