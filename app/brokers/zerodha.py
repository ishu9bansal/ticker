

import datetime
from enum import Enum
from typing import Any
from kiteconnect import KiteConnect

from app.brokers.instruments import INSTRUMENT_STORE
from app.constants import USER_ACCESS_TOKEN, ZERODHA_API_KEY
from app.models.ticker import OptionType, Underlying
from app.utils import timer

class Interval(Enum):
    MINUTE = 'minute'
    DAY = 'day'
    MINUTES3 = '3minute'
    MINUTES5 = '5minute'
    MINUTES10 = '10minute'
    MINUTES15 = '15minute'
    MINUTES30 = '30minute'
    MINUTES60 = '60minute'

def instrumentKey(instrument: dict[str,Any] | None) -> str:
    if not instrument:
        return ""
    return f"{instrument['exchange']}:{instrument['tradingsymbol']}"

def instrumentToken(instrument: dict[str,Any]) -> int:
    return instrument['instrument_token']


class Broker:
    def __init__(self, api_key: str = ZERODHA_API_KEY, access_token: str = USER_ACCESS_TOKEN):
        self.kite = KiteConnect(api_key=api_key, access_token=access_token)
    
    def findOption(self, expiry: str, strike: float, option_type: OptionType, underlying: Underlying) -> dict[str, Any] | None:
        instruments = INSTRUMENT_STORE.instruments()
        instrumentsList = instruments.get(underlying, {}).get(option_type, {}).get(str(expiry), [])
        opts = []
        for ins in instrumentsList:
            if int(round(ins.get("strike", 0))) == int(round(strike)):
                opts.append(ins)
        if not opts:
            return None
        return opts[0]

    def findOptions(self, expiry: str, option_type: OptionType, underlying: Underlying) -> list[Any]:
        instruments = INSTRUMENT_STORE.instruments()
        return instruments.get(underlying, {}).get(option_type, {}).get(str(expiry), [])
    
    def findEarliestExpiry(self, underlying: Underlying) -> str | None:
        instruments = INSTRUMENT_STORE.instruments()
        now = str(datetime.datetime.now())
        expiries: set[str] = set()
        for option_type in instruments.get(underlying, {}):
            for expiry_str in instruments[underlying][option_type]:
                if expiry_str >= now:
                    expiries.add(expiry_str)
        if not expiries:
            return None
        return min(expiries)
    
    def findStock(self, underlying: Underlying) -> dict[str, Any]:
        return INSTRUMENT_STORE.stocks()[underlying]
    
    def instruments(self):
        instruments = INSTRUMENT_STORE.instruments()
        stocks = INSTRUMENT_STORE.stocks()
        # convert nested _instruments to flat array
        insts = [
            ins
            for opt_types in instruments.values()
            for expiries in opt_types.values()
            for ins_list in expiries.values()
            for ins in ins_list
        ]
        insts.extend(stocks.values())
        return insts
    
    @timer
    def profile(self):
        return self.kite.profile()
        
    @timer
    def quote(self, *instruments: str):
        # TODO: make this separate for options and stocks
        return self.kite.quote(instruments)
    
    @timer
    def history(self, instrument_token: int, from_date: datetime.datetime, to_date: datetime.datetime, interval: Interval = Interval.MINUTE):
        return self.kite.historical_data(instrument_token, from_date, to_date, interval.value)
