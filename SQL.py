import sqlite3
import matplotlib.pyplot as plt
import traceback

# Step 1: Create SQLite DB
conn = sqlite3.connect('submissions.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT,
    result TEXT,
    difficulty TEXT
)
''')
conn.commit()

# Step 2: Run code securely
def execute_code(code):
    try:
        local_vars = {}
        exec(code, {}, local_vars)
        return str(local_vars) if local_vars else "Executed Successfully"
    except Exception as e:
        return traceback.format_exc()

# Step 3: Save submission
def save_submission(code, result, difficulty="Unknown"):
    cursor.execute("INSERT INTO submissions (code, result, difficulty) VALUES (?, ?, ?)",
                   (code, result, difficulty))
    conn.commit()

# Step 4: Chart
def plot_solved_problems():
    cursor.execute("SELECT difficulty, COUNT(*) FROM submissions GROUP BY difficulty")
    data = cursor.fetchall()
    difficulties = [row[0] for row in data]
    counts = [row[1] for row in data]

    plt.bar(difficulties, counts, color='skyblue')
    plt.title('Problems Solved by Difficulty')
    plt.xlabel('Difficulty')
    plt.ylabel('Count')
    plt.show()

# TEST: Input code
code = '''
def add(a, b):
    return a + b

x = add(3, 4)
'''
result = execute_code(code)
save_submission(code, result, difficulty="Easy")
print(result)

# View chart
plot_solved_problems()
