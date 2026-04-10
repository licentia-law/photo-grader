from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.analyze import router as analyze_router
from routers.correct import router as correct_router

app = FastAPI(title="Photo Color Grading API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze_router, prefix="/api")
app.include_router(correct_router, prefix="/api")


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Photo Color Grading API is running"}
