from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routers import auth, items, indicators, dashboard

app = FastAPI()


app.mount("/static", StaticFiles(directory="app/static"), name="static")


app.include_router(auth.router)
app.include_router(items.router)
app.include_router(indicators.router)
app.include_router(dashboard.router)