import typing

import datetime as dt 
import polars   as pl 

def data_processing_exceptions(method: typing.Callable):
    def wrapper(self, *args, **kwargs):
        try:
            method(self, *args, **kwargs)
            self.data_log_object.info(f"{str(dt.datetime.now())} - Data processed")
        except pl.exceptions.ColumnNotFoundError as CNFE:
            self.data_log_object.debug(f"{str(dt.datetime.now())} - {CNFE}")
        except FileNotFoundError as FNFE:
            self.data_log_object.debug(f"{str(dt.datetime.now())} - {FNFE}")
        except Exception as E:
            self.data_log_object.debug(f"{str(dt.datetime.now())} - {E}")
    
    return wrapper 

