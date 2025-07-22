import gradio as gr
from translator import translate_code
from analyzer import analyze_code

def launch_interface():
    with gr.Blocks() as app:
        gr.Markdown("# LuminaX-alt 🌐 Code Translation & Analysis")
        
        code_input = gr.Code(label="Enter Code", language="python")
        lang_output = gr.Radio(["Python", "Java", "C++"], label="Convert To", value="Java")
        
        translated_output = gr.Code(label="Translated Code")
        analysis_output = gr.Textbox(label="Code Analysis")

        def process(code, lang):
            translated = translate_code(code, lang)
            analysis = analyze_code(code)
            return translated, analysis

        code_input.change(process, inputs=[code_input, lang_output], outputs=[translated_output, analysis_output])

    app.launch()
