"""
Ticker business logic service.

This module contains the business logic for ticker operations.
"""

from datetime import datetime
from typing import Any
from app.brokers.zerodha import Broker
from app.models.ticker import OptionType, Underlying


class TickerService:
    """Service class for ticker-related business logic."""
    def __init__(self) -> None:
        self.broker = Broker()
    
    def user(self):
        return self.broker.profile()
    
    def instruments(self):
        return self.broker.instruments()
    
    def quote(self, underlying_str: str | None):
        if not underlying_str:
            raise ValueError("Underlying parameter is required")
        u = Underlying(underlying_str)
        return self.broker.quote(self.broker.findStock(u))
    
    def history(self, underlying_str: str | None, from_str: str | None):
        if not underlying_str:
            raise ValueError("Underlying parameter is required")
        if not from_str:
            raise ValueError("From parameter is required, in datetime format YYYY-MM-DDTHH:mm:ss")
        from_date = datetime.fromisoformat(from_str)
        to_date = datetime.now()
        u = Underlying(underlying_str)
        stock_instrument = self.broker.findStock(u)
        return self.broker.history(stock_instrument, from_date, to_date)

    def straddles(self, underlying_str: str | None):
        if not underlying_str:
            raise ValueError("Underlying parameter is required")
        u = Underlying(underlying_str)
        expiry = self.broker.findEarliestExpiry(u)
        if not expiry:
            raise ValueError("Could not find expiry for the given underlying")
        call_instruments = self.broker.findOptions(expiry, OptionType.CALL, u)
        put_instruments = self.broker.findOptions(expiry, OptionType.PUT, u)
        call_map = {ins.get("strike"): ins for ins in call_instruments}
        put_map = {ins.get("strike"): ins for ins in put_instruments}
        common_strikes = set(call_map.keys()).intersection(set(put_map.keys()))
        straddles = []
        for strike in common_strikes:
            id = f'{u.value}:{expiry}:{round(strike)}'
            straddle = {
                "id": id,
                "underlying": u.value,
                "strike": strike,
                "expiry": expiry,
                "call": call_map[strike],
                "put": put_map[strike],
            }
            straddles.append(straddle)
        straddles.sort(key=lambda x: x["strike"])
        return straddles
    
    def straddle_quotes(self, idList: list[str]):
        keys = {}
        for id in idList:
            call_key, put_key = self._straddleKeys(id)
            if not call_key or not put_key:
                raise ValueError(f"Could not find instruments for straddle id {id}")
            keys[call_key] = id
            keys[put_key] = id
        
        quotes = self.broker.quote(*keys.keys())
        
        quote_list_map: dict[str, list] = {}
        for key, quote in quotes.items():
            quote_list_map.setdefault(keys[key], []).append(quote)
        
        return { id: self._combineQuotes(id, quotes) for id, quotes in quote_list_map.items() }
    
    def _combineQuotes(self, id: str, quotes: list[Any]):
        combined = {
            "id": id,
            "timestamp": int(quotes[0]["timestamp"].timestamp()*1000),
            "price": sum(q["last_price"] for q in quotes),
            "quotes": quotes,
        }
        return combined
    
    def _straddleKeys(self, id: str):
        [underlying, expiry, strike_str] = id.split(':')
        u = Underlying(underlying)
        strike = int(strike_str)
        call_key = self.broker.findOptionKey(expiry, strike, OptionType.CALL, u)
        put_key = self.broker.findOptionKey(expiry, strike, OptionType.PUT, u)
        return call_key, put_key
    

