from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import create_db_and_tables
from app.routes import auth_routes, user_routes


app = FastAPI(title="FastAPI Backend")

# Create tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Include Routers
app.include_router(auth_routes.router)
app.include_router(user_routes.router)

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
