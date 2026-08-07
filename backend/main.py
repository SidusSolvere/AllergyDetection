from fastapi import FastAPI

app = FastAPI(
    title="AllergyVision AI",
    version="0.1.0",
    description="Backend API for allergy detection."
)


@app.get("/")
async def root():
    return {
        "message": "AllergyVision AI API is running."
    }