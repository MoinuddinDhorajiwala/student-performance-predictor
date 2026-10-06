# Model Details

- Training records: 5,000
- Target: `Performance_Level`
- Classes: Poor, Average, Good, Excellent
- Model: Multinomial Logistic Regression (C=2)
- Validation split: 80/20 stratified, random_state=42
- Validation accuracy: 98.1%

## Input features

Age, Gender, Class, Study_Hours_Per_Day, Attendance_Percentage,
Parental_Education, Internet_Access, Extracurricular_Activities,
Math_Score, Science_Score, English_Score, Previous_Year_Score.

`Final_Percentage` is not used as a model input because it is the outcome derived from the three current subject scores in the supplied dataset. The UI displays the subject-score average as an estimated final percentage.

## Risk logic

- Poor → High risk
- Average → Medium risk
- Good / Excellent → Low risk

The recommendation engine also checks attendance, study hours, previous-year score and low subject scores to suggest early intervention actions.
