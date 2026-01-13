from fastapi import FastAPI

app = FastAPI(title="Ticker API", version="0.1.0")


@app.get("/")
def read_root():
    """
    Simple Hello World endpoint
    """
    return {"message": "Hello World"}


@app.get("/health")
def health_check():
    """
    Health check endpoint for monitoring
    """
    return {"status": "healthy"}
