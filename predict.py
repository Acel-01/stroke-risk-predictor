import pickle

with open('dv.bin', 'rb') as f_in:
    dv = pickle.load(f_in)

with open('model.bin', 'rb') as f_in:
    model = pickle.load(f_in)

BEST_THRESHOLD = 0.09
MEAN_GLUCOSE = 106.45

def predict_stroke(customer_data):
    """
    Takes a customer dictionary and returns a stroke prediction probability
    and the final decision.
    """
    data = customer_data.copy()
    if data['avg_glucose_level'] is None:
        data['avg_glucose_level'] = MEAN_GLUCOSE

    # We use .transform() on a list containing our single customer
    X = dv.transform([data])

    # Get probability for the "positive" class (class '1')
    y_pred_proba = model.predict_proba(X)[0, 1] 

    decision = (y_pred_proba >= BEST_THRESHOLD)

    return y_pred_proba, decision

if __name__ == "__main__":
    customer = {
        'age': 67.0,
        'gender': 'Female',
        'hypertension': 0,
        'heart_disease': 1,
        'ever_married': 'Yes',
        'work_type': 'Private',
        'residence_type': 'Urban',
        'avg_glucose_level': 228.69,
        'bmi': 36.6,
        'smoking_status': 'formerly smoked'
    }

    # customer = {
    #     'age': 23,
    #     'gender': 'Male',
    #     'hypertension': 0,
    #     'heart_disease': 0,
    #     'ever_married': 'No',
    #     'work_type': 'Private',
    #     'residence_type': 'Urban',
    #     'avg_glucose_level': 228.69,
    #     'bmi': 30.0,
    #     'smoking_status': 'never smoked'
    # }

    probability, prediction = predict_stroke(customer)

    print("--- Prediction Test ---")
    print(f"Customer data: {customer}")
    print(f"Stroke Probability: {probability:.4f}")
    print(f"Stroke Prediction (at {BEST_THRESHOLD} threshold): {prediction}")