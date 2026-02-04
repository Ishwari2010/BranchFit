import pandas as pd
import random
from sklearn.ensemble import RandomForestClassifier
import joblib

# Number of questions
N_QUESTIONS = 60

def generate_student(branch):
    answers = [random.randint(2, 4) for _ in range(N_QUESTIONS)]

    if branch == "Computer Science":
        boost = [2,6,9,11,16,18,23,27,29,30,36,40,43,47,50,55,56]
    elif branch == "Information Technology":
        boost = [6,14,18,21,27,35,44,48,50,56]
    elif branch == "Mechanical":
        boost = [3,5,17,25,37,38,41,45,57,59]
    elif branch == "Electrical":
        boost = [10,12,15,32,33,39,53]
    else:
        boost = []

    for i in boost:
        answers[i] = random.randint(4,5)

    return answers

data = []
labels = []

for _ in range(250):
    data.append(generate_student("Computer Science"))
    labels.append("Computer Science")

for _ in range(250):
    data.append(generate_student("Information Technology"))
    labels.append("Information Technology")

for _ in range(250):
    data.append(generate_student("Mechanical"))
    labels.append("Mechanical")

for _ in range(250):
    data.append(generate_student("Electrical"))
    labels.append("Electrical")

df = pd.DataFrame(data)
df["Branch"] = labels

X = df.drop("Branch", axis=1)
y = df["Branch"]

model = RandomForestClassifier(n_estimators=300, random_state=42)
model.fit(X, y)

joblib.dump(model, "branch_predictor_model.pkl")

print("✅ New model trained and saved!")
