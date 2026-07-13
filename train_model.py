import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pickle

# Load Dataset
data = pd.read_csv("career_data.csv")

# Features and Target
X = data.drop("career", axis=1)
y = data["career"]

# Train Model
model = DecisionTreeClassifier()
model.fit(X, y)

# Save Model
with open("career_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Model Trained Successfully!")