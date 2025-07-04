import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, accuracy_score


df = pd.read_csv("../data/Project_Management_Dataset.csv")
df.columns = df.columns.str.strip()

df["Completion%"] = df["Completion%"].str.replace('%', '').astype(float)
df["Project Cost"] = df["Project Cost"].str.replace(',', '').astype(float)
df["Project Benefit"] = df["Project Benefit"].str.replace(',', '').astype(float)
df["ROI"] = (df["Project Benefit"] - df["Project Cost"]) / df["Project Cost"]
df["Success"] = (df["Completion%"] >= 85).astype(int)

# Features e dummies
features = ["Project Cost", "Project Benefit", "ROI", "Year", "Month"]
df = pd.get_dummies(df, columns=[
    "Complexity", "Region", "Project Type", "Department", "Status", "Phase"
], drop_first=True)

X = df[features + [c for c in df.columns if c.startswith((
    "Complexity_", "Region_", "Project Type_", "Department_", "Status_", "Phase_"))]]
y = df["Success"]


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modelos
models = {
    "Random Forest": RandomForestClassifier(random_state=42),
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric="logloss")
}

# Treinamento e avaliação
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(f"\nModel: {name}")
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))


# Salvar o modelo XGBoost e as colunas usadas
joblib.dump((models["XGBoost"], X.columns.tolist()), "XGBoost.pkl")

