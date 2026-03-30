import uvicorn
import yaml
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from app.database import create_db_and_tables
from app.routes import auth_routes, user_routes, prescription_routes

app = FastAPI(title="FastAPI Backend")


# Create Tables on Startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# Include Routers
app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(prescription_routes.router)

# Disable CORS Error
origins = ["http://localhost:8080"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routes
@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI-Backend server."}


@app.get("/openapi.yaml", response_class=Response, include_in_schema=False)
def get_openapi_yaml():
    openapi_spec = app.openapi()
    openapi_yaml = yaml.dump(openapi_spec, default_flow_style=False)
    return Response(content=openapi_yaml, media_type="application/x-yaml")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
