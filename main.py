from fastapi import FastAPI, Query
import joblib, os
from minio import Minio

app = FastAPI()

# MODEL_PATH = "/artifacts/model.pkl"

# # Load Model on startup
# model = None
# if os.path.exists(MODEL_PATH):
#     model = joblib.load(MODEL_PATH)
# else: 
#     print("No model found yet. Run fraud-trainer svc to generate a model...")

client = Minio(
    "minio.infra.svc.cluster.local:9000",
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=False
)

BUCKET = "fraud-models"
client.fget_object(BUCKET, "model.pkl", "/tmp/model.pkl")

model = joblib.load("/tmp/model.pkl")

@app.get("/predict")
def predict(amount: float = Query(..., description="Transaction amount")):
    global model
    if model is None:
        return {"error": "Model is not available! Please train the model first."}

    prediction = model.predict([[amount]])[0]
    return {
        "amount": amount,
        "is_fraud": bool(prediction)
    }