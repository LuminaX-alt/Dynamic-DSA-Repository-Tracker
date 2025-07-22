# ✅ Install required libraries
!pip install transformers sentencepiece gradio -q

# ✅ Import Libraries
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import gradio as gr

# ✅ Load CodeT5+ Model
model_name = "Salesforce/codet5p-220m"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# ✅ Translation Prompt Builder
def build_prompt(code, source_lang, target_lang):
    return f"Translate the following {source_lang} code to {target_lang}:\n{code}"

# ✅ Translator Function
def translate_code(code, source_lang, target_lang):
    if source_lang == target_lang:
        return "Source and target languages are the same."
    prompt = build_prompt(code, source_lang, target_lang)
    inputs = tokenizer(prompt, return_tensors="pt", padding=True)
    output = model.generate(**inputs, max_length=512, do_sample=True, top_k=50)
    translated_code = tokenizer.decode(output[0], skip_special_tokens=True)
    return translated_code.strip()

# ✅ Gradio UI
def ui_function(code, source_lang, target_lang):
    translated = translate_code(code, source_lang, target_lang)
    return code, translated

langs = ["Python", "Java", "C++"]

gr.Interface(
    fn=ui_function,
    inputs=[
        gr.Textbox(lines=20, label="Input Code"),
        gr.Dropdown(langs, value="Python", label="Source Language"),
        gr.Dropdown(langs, value="Java", label="Target Language")
    ],
    outputs=[
        gr.Code(label="Original Code"),
        gr.Code(label="Translated Code")
    ],
    title="Code Translator - Python ↔ Java ↔ C++",
    description="Uses open-source CodeT5+ model. No API key required."
).launch()
