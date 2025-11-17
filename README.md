# Stroke Risk Prediction API

This is the midterm project for the [ML Zoomcamp](https://github.com/DataTalksClub/machine-learning-zoomcamp), which builds a machine learning model to predict a patient's risk of stroke.

The model is trained, validated, and then served as a REST API using FastAPI and containerized with Docker.

**Final Model Performance (on unseen 20% test set):**
* **ROC-AUC Score:** 0.8514
* **F1-Score (at 0.09 threshold):** 0.2973

---

## 🚀 Live Demo

This project is fully deployed and publicly accessible:

* **Frontend Web App (Streamlit):** **[stroke-risk-predictor-acel.streamlit.app](https://stroke-risk-predictor-acel.streamlit.app/)**
* **Backend API (Google Cloud Run):** **[api.stroke-predictor.acel.dev](https://api.stroke-predictor.acel.dev/)**
* **API Docs (Swagger UI):** **[api.stroke-predictor.acel.dev/docs](https://api.stroke-predictor.acel.dev/docs)**

## 1. Problem Statement

The aim of this project is to build a model that accurately predicts the likelihood of a person having a stroke. It is trained on a public dataset from Kaggle. The goal is to create a tool that an average person could use to get a preliminary risk assessment based on their current health attributes and lifestyle habits.

This is a **binary classification** problem with a **highly imbalanced dataset** (only ~4.8% of cases are "stroke"). Because of this imbalance, **Accuracy** is a misleading metric. The primary metrics used for evaluation are **ROC-AUC** (for overall ranking) and **F1-Score** (for a balance of Precision and Recall).

## 2. Dataset

The dataset used for this project is the [Stroke Prediction Dataset from Kaggle](https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset).

It contains 11 features (inputs) and 1 target variable (`stroke`).

**Features:**
* `gender`
* `age`
* `hypertension`
* `heart_disease`
* `ever_married`
* `work_type`
* `residence_type`
* `avg_glucose_level` (This field is optional in the API)
* `bmi`
* `smoking_status`

## 3. Modeling and Evaluation

1.  **Exploratory Data Analysis (EDA):**
    * The `bmi` column had ~200 missing values, which were filled with the mean.
    * The `smoking_status` column had ~1500 "Unknown" values, which were treated as a separate category.
    * All column names were standardized to lowercase.
    * The `id` column was dropped.

2.  **Model Selection:**
    * Three models were trained and compared: `LogisticRegression`, `RandomForestClassifier`, and `XGBClassifier`.
    * Due to the high class imbalance, the "out-of-the-box" `RandomForest` and `XGBoost` models performed poorly (AUC ~0.76-0.78), as they overfit to the "No Stroke" majority class.
    * The simple `LogisticRegression` baseline achieved the best initial AUC of **0.831**.

3.  **Model Tuning:**
    * Both `LogisticRegression` (tuning `C`) and `XGBoost` (tuning `scale_pos_weight` and other parameters) were tuned.
    * Both tuned models achieved a similar final F1-Score (~0.24-0.25) and ROC-AUC (~0.84).
    * The **Tuned Logistic Regression (C=35)** was chosen as the final model because it provides the same performance as the complex XGBoost model while being **simpler, faster to train, and fully interpretable** (not a "black box").
    * The optimal prediction threshold was found to be **0.09** to achieve the best F1-Score.

---

## 4. How to Run This Project

You can run this project either locally using `uv` or in a container using `Docker`.

### Option 1: Running Locally (with uv)

1.  **Clone the repository:**
    ```bash
    git clone git@github.com:Acel-01/stroke-risk-predictor.git
    cd stroke-risk-predictor
    ```

2.  **Create the environment and install dependencies:**
    ```bash
    uv venv
    source .venv/bin/activate
    uv pip sync
    ```

3.  **Run the API server:**
    ```bash
    uvicorn serve:app --host 0.0.0.0 --port 8000
    ```

### Option 2: Running with Docker (Recommended)

1.  **Build the Docker image:**
    ```bash
    docker build -t stroke-predictor-api .
    ```

2.  **Run the Docker container:**
    ```bash
    docker run --rm -p 8000:8000 --name stroke_predictor stroke-predictor-api
    ```

---

## 5. API Usage

The server is now running at `http://127.0.0.1:8000`.

### Interactive Docs (Swagger UI)

You can access the interactive Swagger documentation by navigating to:
**`http://127.0.0.1:8000/docs`**

From there, you can see all the valid inputs (including dropdowns for categorical features) and test the API.

### Example `curl` Request

Here is an example of how to send a request from your terminal:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
        "age": 67,
        "gender": "Female",
        "hypertension": 0,
        "heart_disease": 1,
        "ever_married": "Yes",
        "work_type": "Private",
        "residence_type": "Urban",
        "avg_glucose_level": 228.69,
        "bmi": 36.6,
        "smoking_status": "formerly smoked"
      }'