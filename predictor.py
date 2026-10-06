import json, math
from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parent / "model" / "model.json"
with MODEL_PATH.open("r", encoding="utf-8") as f:
    MODEL = json.load(f)

CLASSES = MODEL["classes"]
CAT_COLS = MODEL["categorical_columns"]
NUM_COLS = MODEL["numeric_columns"]
CATEGORIES = MODEL["categories"]
MEANS = MODEL["numeric_mean"]
SCALES = MODEL["numeric_scale"]
COEF = MODEL["coef"]
INTERCEPT = MODEL["intercept"]

def _one_hot(data):
    values = []
    for col in CAT_COLS:
        val = str(data.get(col, ""))
        cats = CATEGORIES[col]
        values.extend([1.0 if val == c else 0.0 for c in cats])
    return values

def _features(data):
    vals = _one_hot(data)
    for col in NUM_COLS:
        x = float(data[col])
        scale = SCALES[col] or 1.0
        vals.append((x - MEANS[col]) / scale)
    return vals

def predict_student(data):
    x = _features(data)
    scores = []
    for row, bias in zip(COEF, INTERCEPT):
        scores.append(bias + sum(w * v for w, v in zip(row, x)))
    m = max(scores)
    exps = [math.exp(s - m) for s in scores]
    total = sum(exps)
    probs = [e / total for e in exps]
    idx = max(range(len(probs)), key=probs.__getitem__)
    level = CLASSES[idx]

    math_score = float(data["Math_Score"])
    science_score = float(data["Science_Score"])
    english_score = float(data["English_Score"])
    predicted_percentage = round((math_score + science_score + english_score) / 3.0, 2)

    pass_fail = "Fail" if level == "Poor" else "Pass"
    confidence = round(probs[idx] * 100, 2)

    attendance = float(data["Attendance_Percentage"])
    study = float(data["Study_Hours_Per_Day"])
    previous = float(data["Previous_Year_Score"])

    recommendations = []
    if attendance < 75:
        recommendations.append("Improve attendance and maintain regular class participation.")
    if study < 2.5:
        recommendations.append("Increase focused study time to at least 2.5 hours per day.")
    if previous < 60:
        recommendations.append("Review previous-year fundamentals and weak topics.")
    if min(math_score, science_score, english_score) < 50:
        recommendations.append("Give additional practice to the subject with the lowest score.")
    if not recommendations:
        recommendations.append("Maintain the current study routine and continue regular revision.")

    risk = {
        "Poor": "High",
        "Average": "Medium",
        "Good": "Low",
        "Excellent": "Low"
    }.get(level, "Medium")

    return {
        "performance_level": level,
        "pass_fail": pass_fail,
        "predicted_percentage": predicted_percentage,
        "confidence": confidence,
        "risk": risk,
        "recommendations": recommendations
    }
