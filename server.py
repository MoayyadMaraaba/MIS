from fastapi import FastAPI
from typing import Union
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# import routes
from routes.Authentication import router as authentication_router
from routes.Authorization import router as authorization_router
from routes.Cases import router as cases_router
from routes.Incidents import router as incidents_router

app = FastAPI()

# routers
app.include_router(authentication_router, prefix="/Authentication", tags=["Authentication"])
app.include_router(authorization_router, prefix="/Authorization", tags=["Authorization"])
app.include_router(cases_router, prefix="/Cases", tags=["Cases"])
app.include_router(incidents_router, prefix="/Reports", tags=["Reports"])



from fastapi.responses import FileResponse

app.mount("/uploads/evidence", StaticFiles(directory="uploads/evidence"), name="uploads/evidence")


# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# root endpoint
@app.get("/")
def root():
    return {"Hello": "Moayyad"}