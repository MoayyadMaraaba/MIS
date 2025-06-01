from fastapi import FastAPI
from typing import Union

# import routes
from routes.Authentication import router as authentication_router
from routes.Authorization import router as authorization_router

app = FastAPI()

# routers
app.include_router(authentication_router, prefix="/Authentication", tags=["Authentication"])
app.include_router(authorization_router, prefix="/Authorization", tags=["Authorization"])

# Middleware


# root endpoint
@app.get("/")
def root():
    return {}