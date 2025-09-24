# -*- coding: utf-8 -*-

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from application.config import settings
from db.postgres import db
from fastapi_keycloak import FastAPIKeycloak

from routes import test



# FastAPI-App
app = FastAPI(title="Imkerei Backend")


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.client_origin_url],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(test.router)

# Server-Start
if __name__ == "__main__":
    uvicorn.run("application.main:app", host="0.0.0.0", port=settings.port, reload=settings.reload)
