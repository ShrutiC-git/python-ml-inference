from fastapi import FastAPI, Query
import joblib, os

app = FastAPI()

MODEL_PATH = "/artifacts/model.pkl"

# Load Model on startup
model = None
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else: 
    print("No model found yet. Run fraud-trainer svc to generate a model...")

@app.get("/predict")
def predict(amount: float = Query(..., description="Transaction amount")):
    global model
    if model is None:
        return {"error": "Model not available. Please train the model first."}

    prediction = model.predict([[amount]])[0]
    return {
        "amount": amount,
        "is_fraud": bool(prediction)
    }