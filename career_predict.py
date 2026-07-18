import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib

# Load dataset
df = pd.read_csv("career_dataset.csv")

X = df[["maths", "programming", "communication", "problem_solving"]]
y = df["career"]

# Train Model
model = DecisionTreeClassifier(random_state=42)
model.fit(X, y)

# Save model
joblib.dump(model, "career_model.pkl")

print("Model trained successfully!")