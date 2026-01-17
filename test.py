from app.services.ticker_service import TickerService


service = TickerService()

def main():
    # straddles = service.straddles("NIFTY")
    # print([s.get("id") for s in straddles])
    quote = service.straddle_quotes(["NIFTY:2026-01-20:23950"])
    print(quote)
    
    

if __name__ == "__main__":
    main()
    