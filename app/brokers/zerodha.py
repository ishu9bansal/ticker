

import datetime
from enum import Enum
from typing import Any
from kiteconnect import KiteConnect

from app.constants import USER_ACCESS_TOKEN, ZERODHA_API_KEY
from app.models.ticker import OptionType, Underlying
from app.utils import cached, timer

TRADING_SYMBOL = {
    "NIFTY 50": Underlying.NIFTY,
    "SENSEX": Underlying.SENSEX,
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

def instrumentKey(instrument: dict[str,Any] | None) -> str:
    if not instrument:
        return ""
    return f"{instrument['exchange']}:{instrument['tradingsymbol']}"

def instrumentToken(instrument: dict[str,Any]) -> int:
    return instrument['instrument_token']


class Broker:
    _instruments: dict[Underlying, dict[OptionType, dict[str, list[dict[str, Any]]]]] = {}
    _stocks: dict[Underlying, dict[str, Any]] = {}
    
    @timer
    def __init__(self, api_key: str = ZERODHA_API_KEY, access_token: str = USER_ACCESS_TOKEN):
        self.kite = KiteConnect(api_key=api_key, access_token=access_token)
        self._instruments, self._stocks = self.__instruments_init("cache_key")
    
    @cached('zerodha_instruments')
    def __instruments_init(self, _: str):
        instruments = self.kite.instruments()
        return self._preprocessInstruments(instruments)
    
    @timer
    def _preprocessInstruments(self, allInstruments):
        # Filter only supported underlyings
        supportedUnderlyings = {u.value for u in Underlying}
        
        # Filter only options type instruments
        supportedTypes = {o.value for o in OptionType}
        
        def filterOptions(ins: dict[str, str]) -> bool:
            return ins.get("name") in supportedUnderlyings and ins.get("instrument_type") in supportedTypes

        def filterStocks(ins: dict[str, str]) -> bool:
            return ins.get("tradingsymbol") in TRADING_SYMBOL
        
        instruments = {}
        option_instruments = [ins for ins in allInstruments if filterOptions(ins)]
        for ins in option_instruments:
            underlying = Underlying(ins.get("name"))
            optionType = OptionType(ins.get("instrument_type"))
            expiry = str(ins.get("expiry"))
            if underlying not in instruments:
                instruments[underlying] = {}
            if optionType not in instruments[underlying]:
                instruments[underlying][optionType] = {}
            if expiry not in instruments[underlying][optionType]:
                instruments[underlying][optionType][expiry] = []
            instruments[underlying][optionType][expiry].append(ins)
        
        stocks = {}
        stock_instruments = [ins for ins in allInstruments if filterStocks(ins)]
        for ins in stock_instruments:
            stocks[TRADING_SYMBOL[ins.get("tradingsymbol")]] = ins
        
        return instruments, stocks
    
    def findOption(self, expiry: str, strike: float, option_type: OptionType, underlying: Underlying) -> dict[str, Any] | None:
        instruments = self._instruments.get(underlying, {}).get(option_type, {}).get(str(expiry), [])
        opts = []
        for ins in instruments:
            if int(round(ins.get("strike", 0))) == int(round(strike)):
                opts.append(ins)
        if not opts:
            return None
        return opts[0]

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
    
    def findStock(self, underlying: Underlying) -> dict[str, Any]:
        return self._stocks[underlying]
    
    def instruments(self):
        # convert nested _instruments to flat array
        insts = [
            ins
            for opt_types in self._instruments.values()
            for expiries in opt_types.values()
            for ins_list in expiries.values()
            for ins in ins_list
        ]
        insts.extend(self._stocks.values())
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
