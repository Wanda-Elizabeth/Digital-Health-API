from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes import patients_router, encounters_router

app = FastAPI(title="Digital Health API", version="1.0")

#  CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables once at startup (good for dev)
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# Routers
app.include_router(patients_router, prefix="/api/patients", tags=["patients"])
app.include_router(encounters_router, prefix="/api/encounters", tags=["encounters"])

@app.get("/")
def read_root():
    return {"message": "Digital Health API is LIVE!"}
