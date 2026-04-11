import uvicorn
import yaml
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from app.database import create_db_and_tables
from app.routes import (
    appointment_routes,
    auth_routes,
    cart_routes,
    chatbot_routes,
    customer_routes,
    doctor_routes,
    feedback_routes,
    inventory_routes,
    medicine_request_routes,
    medicines_routes,
    order_routes,
    overview_routes,
    prescription_routes,
    staff_routes,
    user_routes,
)
from app.seed import seed_data

app = FastAPI(title="FastAPI Backend")


# Create Tables on Startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    seed_data()


# Include Routers
api_router = APIRouter(prefix="/api")

api_router.include_router(auth_routes.router)
api_router.include_router(user_routes.router)
api_router.include_router(prescription_routes.router)
api_router.include_router(doctor_routes.router)
api_router.include_router(appointment_routes.router)
api_router.include_router(medicines_routes.router)
api_router.include_router(overview_routes.router)
api_router.include_router(chatbot_routes.router)

api_router.include_router(inventory_routes.router)
api_router.include_router(order_routes.router)
api_router.include_router(cart_routes.router)
api_router.include_router(medicine_request_routes.router)
api_router.include_router(staff_routes.router)
api_router.include_router(customer_routes.router)
api_router.include_router(feedback_routes.router)

app.include_router(api_router)

# Disable CORS Error
origins = ["http://localhost:8080"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
