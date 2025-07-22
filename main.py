!pip install gradio pandas scikit-learn
from google.colab import files
uploaded = files.upload()
import zipfile
import os

# Assuming only one zip is uploaded
zip_path = list(uploaded.keys())[0]

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall('unzipped_dataset')

# See extracted files
os.listdir('unzipped_dataset')
from google.colab import files

uploaded = files.upload()  # You'll be prompted to select the CSV file
import pandas as pd

# Automatically get the uploaded file name
import os
uploaded_files = os.listdir()
csv_file = [f for f in uploaded_files if f.endswith('.csv')][0]  # picks the first .csv file

# Load the dataset
df = pd.read_csv(csv_file)

# Preview
df.head()
import pandas as pd
import os

# Automatically pick the uploaded CSV
csv_file = [f for f in os.listdir() if f.endswith('.csv')][0]
df = pd.read_csv(csv_file)

# Preview
df.head()
print(df.columns.tolist())
df = df[['title', 'difficulty', 'related_topics', 'description']].rename(columns={'related_topics': 'tags'}).dropna()
df.head()
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle

# Combine description and tags into a single text field
df['text'] = df['description'] + ' ' + df['tags']

# Encode difficulty (Easy=0, Medium=1, Hard=2)
label_encoder = LabelEncoder()
df['difficulty_encoded'] = label_encoder.fit_transform(df['difficulty'])

# Vectorize the combined text
tfidf = TfidfVectorizer(max_features=1000)
X = tfidf.fit_transform(df['text'])
y = df['difficulty_encoded']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train classifier
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model & vectorizer
with open("difficulty_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("tfidf_vectorizer.pkl", "wb") as f:
    pickle.dump(tfidf, f)

print("✅ Model trained and saved!")
import ast

def estimate_time_complexity(code):
    try:
        tree = ast.parse(code)
        loop_count = sum(isinstance(node, (ast.For, ast.While)) for node in ast.walk(tree))
        functions = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
        recursion = any(
            isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in functions
            for node in ast.walk(tree)
        )

        if recursion:
            return "O(2^n) or O(n^2) [Recursive]"
        if loop_count == 0:
            return "O(1)"
        elif loop_count == 1:
            return "O(n)"
        elif loop_count == 2:
            return "O(n^2)"
        else:
            return f"O(n^{loop_count})"
    except Exception as e:
        return f"Error estimating complexity: {e}"
from sklearn.metrics.pairwise import cosine_similarity

def get_similar_problems(problem_title, top_k=3):
    idx = df[df['title'] == problem_title].index[0]
    vec = X[idx]
    similarities = cosine_similarity(vec, X).flatten()
    similar_indices = similarities.argsort()[::-1][1:top_k+1]
    return df.iloc[similar_indices][['title', 'tags', 'difficulty']].to_dict(orient='records')
import sqlite3

# Create DB connection
conn = sqlite3.connect('user_activity.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS activity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    problem_title TEXT,
    code TEXT,
    predicted_difficulty TEXT,
    time_complexity TEXT,
    solved_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
conn.commit()
import gradio as gr

def analyze_submission(username, problem_title, user_code):
    # Vectorize problem description
    desc = df[df['title'] == problem_title]['text'].values[0]
    vec = tfidf.transform([desc])

    # Predict difficulty
    difficulty_pred = label_encoder.inverse_transform(model.predict(vec))[0]

    # Estimate time complexity
    time_comp = estimate_time_complexity(user_code)

    # Store in DB
    cursor.execute(
        "INSERT INTO activity (username, problem_title, code, predicted_difficulty, time_complexity) VALUES (?, ?, ?, ?, ?)",
        (username, problem_title, user_code, difficulty_pred, time_comp)
    )
    conn.commit()

    # Recommendations
    recs = get_similar_problems(problem_title)

    result = f"🔹 Predicted Difficulty: {difficulty_pred}\n🔹 Estimated Time Complexity: {time_comp}"
    return result, recs

# Gradio UI
demo = gr.Interface(
    fn=analyze_submission,
    inputs=[
        gr.Textbox(label="Username"),
        gr.Dropdown(choices=list(df['title']), label="Select Problem"),
        gr.Code(language="python", label="Paste Your Code")
    ],
    outputs=[
        gr.Textbox(label="AI Feedback"),
        gr.JSON(label="🔁 Recommended Problems")
    ],
    title="🧠 Dynamic DSA Practice Tracker"
)

demo.launch()

