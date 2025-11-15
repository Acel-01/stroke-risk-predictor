from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from predict import predict_stroke
from schemas import Customer

# --- Initialize our FastAPI app ---
app = FastAPI(
    title="Stroke Prediction API",
    description="An API to predict stroke risk based on patient health data."
)

@app.post("/predict", summary="Predict stroke risk")
def predict(customer: Customer):
    """
    This is the function that gets called when a user
    sends a POST request to our /predict URL.
    """
    customer_dict = jsonable_encoder(customer)
    probability, decision = predict_stroke(customer_dict)
    return {
        "stroke_probability": float(probability),
        "stroke_prediction": bool(decision)
    }

# health check endpoint
@app.get("/", summary="Health check")
def health_check():
    return {"status": "ok", "message": "Stroke prediction service is running."}