from fastapi import FastAPI
from app.api import routes
from app.db import session, base, models
import os

app = FastAPI(title="Trading Backtest API")

app.include_router(routes.router)

@app.on_event("startup")
def startup():
    # create DB file / tables
    base.Base.metadata.create_all(bind=session.engine)
