

import datetime
from enum import Enum
from typing import Any
from app.constants import USER_ACCESS_TOKEN, ZERODHA_API_KEY
from kiteconnect import KiteConnect

from app.models.ticker import OptionType, Underlying

INSTRUMENT_MAP = {
    Underlying.NIFTY: "NSE:NIFTY 50",
    Underlying.SENSEX: "BSE:SENSEX",
}

class Interval(Enum):
    MINUTE = 'minute'
    DAY = 'day'
    MINUTES3 = '3minute'
    MINUTES5 = '5minute'
    MINUTES10 = '10minute'
    MINUTES15 = '15minute'
    MINUTES30 = '30minute'
    MINUTES60 = '60minute'

def instrumentKey(instrument: dict[str,str]) -> str:
    return f"{instrument['exchange']}:{instrument['tradingsymbol']}"


class Broker:
    _instruments: dict[Underlying, dict[OptionType, dict[str, list[dict[str, Any]]]]] = {}
    def __init__(self, api_key: str = ZERODHA_API_KEY, access_token: str = USER_ACCESS_TOKEN):
        self.kite = KiteConnect(api_key=api_key, access_token=access_token)
        self._preprocessInstruments(self.kite.instruments())
    
    def _preprocessInstruments(self, allInstruments) -> None:
        # Filter only supported underlyings
        supportedUnderlyings = {u.value for u in Underlying}
        
        # Filter only options type instruments
        supportedTypes = {o.value for o in OptionType}
        
        def filterFunc(ins: dict[str, str]) -> bool:
            return ins.get("name") in supportedUnderlyings and ins.get("instrument_type") in supportedTypes
        
        instruments = [ins for ins in allInstruments if filterFunc(ins)]
        for ins in instruments:
            underlying = Underlying(ins.get("name"))
            optionType = OptionType(ins.get("instrument_type"))
            expiry = str(ins.get("expiry"))
            if underlying not in self._instruments:
                self._instruments[underlying] = {}
            if optionType not in self._instruments[underlying]:
                self._instruments[underlying][optionType] = {}
            if expiry not in self._instruments[underlying][optionType]:
                self._instruments[underlying][optionType][expiry] = []
            self._instruments[underlying][optionType][expiry].append(ins)
    
    def findOptionKey(self, expiry: str, strike: float, option_type: OptionType, underlying: Underlying) -> str | None:
        instruments = self._instruments.get(underlying, {}).get(option_type, {}).get(str(expiry), [])
        opts = []
        for ins in instruments:
            if int(round(ins.get("strike", 0))) == int(round(strike)):
                opts.append(ins)
        if not opts:
            return None
        return instrumentKey(opts[0])

    def findOptions(self, expiry: str, option_type: OptionType, underlying: Underlying) -> list[Any]:
        return self._instruments.get(underlying, {}).get(option_type, {}).get(str(expiry), [])
    
    def findEarliestExpiry(self, underlying: Underlying) -> str | None:
        now = str(datetime.datetime.now())
        expiries: set[str] = set()
        for option_type in self._instruments.get(underlying, {}):
            for expiry_str in self._instruments[underlying][option_type]:
                if expiry_str >= now:
                    expiries.add(expiry_str)
        if not expiries:
            return None
        return min(expiries)
    
    def findStock(self, underlying: Underlying) -> str:
        return INSTRUMENT_MAP[underlying]
    
    def instruments(self):
        # convert nested _instruments to flat array
        return [
            ins
            for opt_types in self._instruments.values()
            for expiries in opt_types.values()
            for ins_list in expiries.values()
            for ins in ins_list
        ]
    
    def profile(self):
        return self.kite.profile()
        
    def quote(self, *instruments: str):
        return self.kite.quote(instruments)
    
    def history(self, instrument: str, from_date: datetime.datetime, to_date: datetime.datetime, interval: Interval = Interval.MINUTE):
        return self.kite.historical_data(instrument, from_date, to_date, interval.value)
