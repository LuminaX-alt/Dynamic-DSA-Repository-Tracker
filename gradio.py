import gradio as gr
import sqlite3
import ast
import pygments
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

# ---------- SQLite Setup ----------
conn = sqlite3.connect("dsa_tracker.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS dsa_problems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    language TEXT,
    code TEXT
)
""")
conn.commit()

# ---------- Helper Functions ----------
def save_code(title, language, code):
    cursor.execute("INSERT INTO dsa_problems (title, language, code) VALUES (?, ?, ?)", (title, language, code))
    conn.commit()
    return "✅ Saved successfully!"

def view_stats():
    cursor.execute("SELECT language, COUNT(*) FROM dsa_problems GROUP BY language")
    stats = cursor.fetchall()
    return "\n".join([f"{lang}: {count} problems" for lang, count in stats]) or "No entries yet."

def syntax_highlight(code):
    return pygments.highlight(code, PythonLexer(), HtmlFormatter(full=True, style="colorful"))

def analyze_code_structure(code):
    try:
        tree = ast.parse(code)
        function_count = len([n for n in tree.body if isinstance(n, ast.FunctionDef)])
        loop_count = len([n for n in ast.walk(tree) if isinstance(n, (ast.For, ast.While))])
        if_count = len([n for n in ast.walk(tree) if isinstance(n, ast.If)])
        return f"📊 Analysis:\n- Functions: {function_count}\n- Loops: {loop_count}\n- Conditionals: {if_count}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def translate_code(code, src, tgt):
    # Dummy placeholder: Replace with real translation logic
    return f"🔄 Code translation from {src} to {tgt} is under development."

# ---------- Gradio Interface ----------
with gr.Blocks() as demo:
    gr.Markdown("# 🧠 DSA Problem Tracker + Analyzer")

    with gr.Tab("➕ Add DSA Problem"):
        title = gr.Textbox(label="Problem Title")
        lang = gr.Dropdown(["Python", "Java", "C++"], label="Language")
        code_input = gr.Code(label="Code", language="python")
        output = gr.Textbox(label="Status")
        submit = gr.Button("💾 Save")
        submit.click(save_code, inputs=[title, lang, code_input], outputs=output)

    with gr.Tab("📊 View Stats"):
        stats_btn = gr.Button("📈 Show Stats")
        stats_out = gr.Textbox(label="Language-wise Problem Count")
        stats_btn.click(view_stats, outputs=stats_out)

    with gr.Tab("🔍 Code Analyzer"):
        code_to_analyze = gr.Code(label="Paste Python Code", language="python")
        analyze_btn = gr.Button("📑 Analyze")
        analysis_result = gr.Textbox(label="Result")
        analyze_btn.click(analyze_code_structure, inputs=code_to_analyze, outputs=analysis_result)

    with gr.Tab("🌐 Translate Code"):
        code_translate = gr.Code(label="Enter Source Code", language="python")
        src_lang = gr.Dropdown(["Python", "Java", "C++"], label="From")
        tgt_lang = gr.Dropdown(["Python", "Java", "C++"], label="To")
        translate_btn = gr.Button("🔄 Translate")
        translated_output = gr.Textbox(label="Translated Code")
        translate_btn.click(translate_code, inputs=[code_translate, src_lang, tgt_lang], outputs=translated_output)

demo.launch()
