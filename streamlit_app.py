import streamlit as st
import requests
import json
from schemas import Gender, EverMarried, WorkType, ResidenceType, SmokingStatus


# ---
API_URL = "https://stroke-predictor-api-530767428784.us-east1.run.app/predict" 
# -------------------------------------------------


# 1. Set up the page title
st.set_page_config(page_title="Stroke Risk Predictor", layout="centered")
st.title("Stroke Risk Predictor 🧠")
st.write("Enter your information below to get a prediction on your stroke risk.")

# 2. Create the input widgets for the user
# We'll use columns to make it look clean
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", min_value=1, max_value=120, value=50)
    avg_glucose_level = st.number_input("Average Glucose Level (Optional)", value=None, placeholder="Leave blank if unknown...")
    bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, value=28.0, step=0.1)

    # Use enums for the select boxes
    gender = st.selectbox("Gender", [g.value for g in Gender])
    smoking_status = st.selectbox("Smoking Status", [s.value for s in SmokingStatus])

with col2:
    hypertension = st.selectbox("Hypertension", ["No", "Yes"])
    heart_disease = st.selectbox("Heart Disease", ["No", "Yes"])
    ever_married = st.selectbox("Ever Married?", [e.value for e in EverMarried])
    work_type = st.selectbox("Work Type", [w.value for w in WorkType])
    residence_type = st.selectbox("Residence Type", [r.value for r in ResidenceType])

# 3. Create the "Predict" button
if st.button("Predict Stroke Risk", type="primary"):

    # 4. When clicked, collect the data into a dictionary
    customer_data = {
        "age": age,
        "gender": gender,
        "hypertension": 1 if hypertension == "Yes" else 0,
        "heart_disease": 1 if heart_disease == "Yes" else 0,
        "ever_married": ever_married,
        "work_type": work_type,
        "residence_type": residence_type,
        "avg_glucose_level": avg_glucose_level,
        "bmi": bmi,
        "smoking_status": smoking_status
    }

    # 5. Send the data to your live API
    try:
        with st.spinner("Calculating..."):
            response = requests.post(API_URL, json=customer_data)
            response.raise_for_status() # Raises an error for bad responses

            result = response.json()

            # 6. Display the result
            prob = result["stroke_probability"]
            decision = result["stroke_prediction"]

            if decision:
                st.error("Risk Level: Elevated", icon="⚠️")
                st.metric(label="Your Predicted Probability", value=f"{prob:.2%}")
                st.caption("This probability is in a range that is considered "
                           "high-risk compared to the general population. "
                           "This is not a medical diagnosis. Please consult a doctor "
                           "to discuss your results.")
            else:
                st.success("Risk Level: Low", icon="✅")
                st.metric(label="Your Predicted Probability", value=f"{prob:.2%}")

    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to the API. Error: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
