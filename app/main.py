from fastapi import FastAPI
from app.api.v1 import endpoints

app = FastAPI(title="PDF to Excel Converter API", version="1.0.0")

# Include API routers
app.include_router(endpoints.router, prefix="/api/v1") 