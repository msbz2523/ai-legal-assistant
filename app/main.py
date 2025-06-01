from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import extract_and_summarize

# Create FastAPI application instance
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include only available routers
app.include_router(extract_and_summarize.router)

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "API is running correctly."}