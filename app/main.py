import logging
from datetime import datetime

from fastapi_offline import FastAPIOffline
from sqlalchemy.orm import Session
from app.core.config import settings
from app.api.api_v1.debs import get_db
from fastapi import Depends, HTTPException, status

from app.initial_data import main as init_main
from app.backend_pre_start import main as backend_prestart
# from app.core.logging.logger import CustomLogger

# routers
from app.api.api_v1.api import api_router

app = FastAPIOffline(title=settings.PROJECT_NAME)
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event('startup')
def run_before():
    init_main()
    backend_prestart()


sep = '<>'

print("\n")
print(f'{sep}' * 30)
print(f'{settings.PROJECT_NAME} Started at: {datetime.now()}')
print(f'{sep}' * 30)
print('\n')
