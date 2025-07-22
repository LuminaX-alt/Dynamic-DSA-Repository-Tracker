!pip install gradio pygments

import gradio as gr
from pygments import highlight
from pygments.lexers import PythonLexer, JavaLexer, CppLexer
from pygments.formatters import HtmlFormatter

# Highlighting function
def highlight_code(code, lang):
    lexer = {'Python': PythonLexer(), 'Java': JavaLexer(), 'C++': CppLexer()}.get(lang, PythonLexer())
    formatter = HtmlFormatter(style='colorful', full=True, linenos=True)
    return highlight(code, lexer, formatter)

# Dummy translation (replace this with real translation logic)
def translate_code(code, source_lang, target_lang):
    if source_lang == target_lang:
        return code
    return f"// Translated from {source_lang} to {target_lang}\n" + code[::-1]  # Dummy reverse for effect

# Combine translation and highlighting
def process_code(code, source_lang, target_lang):
    if not code.strip():
        return "Please paste some code first!", "", ""
    translated = translate_code(code, source_lang, target_lang)
    original_highlighted = highlight_code(code, source_lang)
    translated_highlighted = highlight_code(translated, target_lang)
    return original_highlighted, translated_highlighted

# Gradio Interface
iface = gr.Interface(
    fn=process_code,
    inputs=[
        gr.Textbox(lines=20, label="Enter Code"),
        gr.Dropdown(["Python", "Java", "C++"], label="Source Language"),
        gr.Dropdown(["Python", "Java", "C++"], label="Target Language")
    ],
    outputs=[
        gr.HTML(label="Original Code (Highlighted)"),
        gr.HTML(label="Translated Code (Highlighted)")
    ],
    title="Code Translator & Highlighter",
    description="Paste your code, select source & target languages to view highlighted & translated output."
)

iface.launch(share=True)
