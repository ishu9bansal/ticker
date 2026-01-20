from app.services.ticker_service import TickerService

service = TickerService()

def main():
    # straddles = service.straddles("NIFTY")
    # print([s.get("id") for s in straddles])
    # quote = service.straddle_quotes(["NIFTY:2026-01-20:25650"])
    # print(quote)
    # t0 = datetime.datetime(1970, 1, 1, 0, 0, 0, 0)
    # t1 = datetime.datetime(1970, 1, 1, 5, 30, 0, 0, tzinfo=tzoneIndia)
    # print(t0)
    # print(t1)
    # print(int(t0.timestamp() * 1000))
    # print(int(t1.timestamp() * 1000))
    # # print(t1-t0)
    # print(1768894192000 - int(t0.timestamp() * 1000))
    
    history = service.history("NIFTY", "2026-01-20T09:15:00", "2026-01-20T11:15:00")
    print(history)


if __name__ == "__main__":
    main()
