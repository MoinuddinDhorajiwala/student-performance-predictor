# Student Performance Prediction — BDA Mini Project (Project 06)

A lightweight, Vercel-ready web application based on the supplied Student Performance Dataset and EDA notebook.

## Group
- Mohammed Zaid Mirkar (231236)
- Faisal Alvi (231202)
- Mohammad Ibrahim Maniyar (231234)

## Model
Multinomial Logistic Regression trained on 5,000 supplied records to predict:
- Poor
- Average
- Good
- Excellent

Validation accuracy on a stratified 80/20 split: **98.1%**.

The deployed runtime does **not** need pandas or scikit-learn. The trained coefficients and preprocessing metadata are exported to `model/model.json`, and prediction is performed with Python's standard library. This keeps the Vercel function lightweight.

## Run locally

Python 3.10+ is recommended.

1. Open this folder in a terminal.
2. Run:
   `python run_local.py`
3. Open:
   `http://127.0.0.1:8000`

No pip install is required.

## Deploy to Vercel

Push this folder to GitHub and import the repository into Vercel. Vercel detects `api/index.py` as a Python Function and serves `index.html` as the frontend.

API endpoint:
`/api`

The project uses the same-origin API, so no CORS configuration is required.

## Source basis

The supplied project-topic PDF lists Project 06 under Education as "Student performance prediction", with online course interaction logs as the suggested scope, early intervention for at-risk students as the objective, and Python/R/Spark as tools. The supplied dataset/notebook instead contains 5,000 student records with study, attendance, subject-score, previous-score, performance-level and pass/fail fields. This application uses that supplied dataset for the working implementation.
