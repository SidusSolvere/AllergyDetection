from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import numpy as np, cv2
from predictor import AllergyPredictor
from database import SessionLocal, Prediction

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

predictor = AllergyPredictor("allergyDetection.h5")


@app.get("/")
async def root():
    return {"message": "Allergy Detection API is up."}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if file.content_type.split('/')[0] != 'image':
        raise HTTPException(status_code=400, detail="Invalid image file")
    try:
        image_data = await file.read()
        img = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            raise HTTPException(status_code=400, detail="Image decoding failed")
        return predictor.predict(img)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
        cnn_result = predictor.predict(img)

        db = SessionLocal()
        db.add(Prediction(result=cnn_result["result"], severity_percentage=cnn_result["severity_percentage"]))
        db.commit()
        db.close()

        return cnn_result

@app.get("/history")
async def history():
    db = SessionLocal()
    rows = db.query(Prediction).order_by(Prediction.created_at.desc()).limit(20).all()
    db.close()
    return [{"result": r.result, "severity_percentage": r.severity_percentage, "created_at": r.created_at} for r in rows]