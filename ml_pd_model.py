import numpy as np
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, roc_curve, auc

np.random.seed(42)
data_size = 700

data = pd.DataFrame({
    "DSCR": np.random.uniform(0.5, 3.0, data_size),
    "Debt_to_Equity": np.random.uniform(0.1, 3.0, data_size),
    "Revenue": np.random.uniform(1e6, 1e7, data_size)
})

data["Default"] = (
    (data["DSCR"] < 1.2) |
    (data["Debt_to_Equity"] > 2.0)
).astype(int)

X = data[["DSCR", "Debt_to_Equity", "Revenue"]]
y = data["Default"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, random_state=42, stratify=y
)

model_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000))
])

model_pipeline.fit(X_train, y_train)

y_pred = model_pipeline.predict(X_test)
y_prob = model_pipeline.predict_proba(X_test)[:, 1]

_accuracy = accuracy_score(y_test, y_pred)
_cm = confusion_matrix(y_test, y_pred)
_fpr, _tpr, _ = roc_curve(y_test, y_prob)
_roc_auc = auc(_fpr, _tpr)

def predict_probability_of_default(metrics):
    input_data = pd.DataFrame([{
        "DSCR": float(metrics.get("DSCR", 0.0)),
        "Debt_to_Equity": float(metrics.get("Debt_to_Equity", 0.0)),
        "Revenue": float(metrics.get("Revenue", 0.0))
    }])

    probability = model_pipeline.predict_proba(input_data)[0][1]
    return round(probability * 100, 2)

def get_model_metrics():
    return _accuracy, _cm, _fpr, _tpr, _roc_auc
