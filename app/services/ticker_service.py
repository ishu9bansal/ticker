"""
Ticker business logic service.

This module contains the business logic for ticker operations.
"""

from datetime import datetime
from typing import Any
from app.brokers.zerodha import Broker, instrumentKey, instrumentToken
from app.constants import TZONE_INDIA
from app.models.ticker import OptionType, Underlying
from app.utils import timer


class TickerService:
    """Service class for ticker-related business logic."""
    def __init__(self) -> None:
        self.broker = Broker()
    
    @timer
    def user(self):
        return self.broker.profile()
    
    @timer
    def instruments(self):
        return self.broker.instruments()
    
    @timer
    def quote(self, underlying_str: str | None):
        if not underlying_str:
            raise ValueError("Underlying parameter is required")
        u = Underlying(underlying_str)
        stock = self.broker.findStock(u)
        key = instrumentKey(stock)
        quote_map = self.broker.quote(key)
        quote = quote_map.get(key)
        return { u.value: self._combineQuotes(u.value, [quote]) }
    
    @timer
    def history(self, underlying_str: str | None, from_str: str | None, to_str: str | None = None):
        if not underlying_str:
            raise ValueError("Underlying parameter is required")
        if not from_str:
            raise ValueError("From parameter is required, in datetime format YYYY-MM-DDTHH:mm:ss")
        from_date = datetime.fromisoformat(from_str)
        to_date = datetime.fromisoformat(to_str) if to_str else datetime.now()
        u = Underlying(underlying_str)
        token = instrumentToken(self.broker.findStock(u))
        history = self.broker.history(token, from_date, to_date)
        parsed_records = [self._parseHistoryRecord([record]) for record in history]
        sorted_records = sorted(parsed_records, key=lambda x: x["timestamp"])
        return { underlying_str: sorted_records }
    
    @timer
    def straddleHistory(self, straddle_id: str | None, from_str: str | None, to_str: str | None = None):
        if not straddle_id:
            raise ValueError("straddle parameter is required")
        if not from_str:
            raise ValueError("From parameter is required, in datetime format YYYY-MM-DDTHH:mm:ss")
        call_opt, put_opt = self._straddleInsts(straddle_id)
        if not call_opt or not put_opt:
            raise ValueError("Could not find instruments for the given straddle id")
        call_token, put_token = instrumentToken(call_opt), instrumentToken(put_opt)
        from_date = datetime.fromisoformat(from_str)
        to_date = datetime.fromisoformat(to_str) if to_str else datetime.now()
        call_history = self.broker.history(call_token, from_date, to_date)
        put_history = self.broker.history(put_token, from_date, to_date)
        # Combine call and put history by timestamp
        call_map = {record["date"]: record for record in call_history}
        put_map = {record["date"]: record for record in put_history}
        common_timestamps = set(call_map.keys()).intersection(set(put_map.keys()))
        combined_history = { ts: [call_map[ts], put_map[ts]] for ts in common_timestamps }
        parsed_records = [self._parseHistoryRecord(records) for records in combined_history.values()]
        sorted_records = sorted(parsed_records, key=lambda x: x["timestamp"])
        return { straddle_id: sorted_records }
    
    def _parseHistoryRecord(self, records: list[dict[str, Any]]) -> dict[str, Any]:
        # TODO: create a pydantic model for this
        tzone_aware_time: datetime = records[0]["date"]
        parsed = {
            "tstring": tzone_aware_time.isoformat(),
            "timestamp": int(tzone_aware_time.timestamp()*1000),
            "open": sum(float(record["open"]) for record in records),
            "high": sum(float(record["high"]) for record in records),
            "low": sum(float(record["low"]) for record in records),
            "close": sum(float(record["close"]) for record in records),
            "volume": sum(float(record["volume"]) for record in records),
            "records": records,
        }
        return parsed

    @timer
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
    
    @timer
    def straddle_quotes(self, idList: list[str]):
        keys = {}
        for id in idList:
            call_opt, put_opt = self._straddleInsts(id)
            call_key, put_key = instrumentKey(call_opt), instrumentKey(put_opt)
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
        # TODO: create a pydantic model for this
        naive_time: datetime = quotes[0]["timestamp"]
        tzone_aware_time = naive_time.replace(tzinfo=TZONE_INDIA)
        combined = {
            "id": id,
            "tstring": tzone_aware_time.isoformat(),
            "timestamp": int(tzone_aware_time.timestamp()*1000),
            "price": sum(q["last_price"] for q in quotes),
            "quotes": quotes,
        }
        return combined
    
    def _straddleInsts(self, id: str):
        [underlying, expiry, strike_str] = id.split(':')
        u = Underlying(underlying)
        strike = int(strike_str)
        call_opt = self.broker.findOption(expiry, strike, OptionType.CALL, u)
        put_opt = self.broker.findOption(expiry, strike, OptionType.PUT, u)
        return call_opt, put_opt
    

