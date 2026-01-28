
from typing import Any

from kiteconnect import KiteConnect
from app.brokers.zerodha import TRADING_SYMBOL
from app.constants import ZERODHA_API_KEY
from app.models.ticker import OptionType, Underlying
from app.utils.decorators import timer


class InstrumentStore:
    """Class to cache and retrieve instrument data."""
    _instruments: dict[Underlying, dict[OptionType, dict[str, list[dict[str, Any]]]]]
    _stocks: dict[Underlying, dict[str, Any]]
    
    def __init__(self, api_key: str = ZERODHA_API_KEY):
        self.api_key = api_key
        self.load()
    
    def instruments(self):
        if not self._instruments:
            self.load()
        return self._instruments
    
    def stocks(self):
        if not self._stocks:
            self.load()
        return self._stocks
    
    @classmethod
    def singleton(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls()
        return cls._instance
    
    def load(self):
        kite = KiteConnect(api_key=self.api_key)
        instruments = kite.instruments()
        self._instruments, self._stocks = self._preprocessInstruments(instruments)
    
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

# Export a singleton instance
INSTRUMENT_STORE = InstrumentStore.singleton()
