!pip install gpt4all
from gpt4all import GPT4All

def explain_code_locally(code_str):
    model = GPT4All("ggml-gpt4all-j-v1.3-groovy")  # you can also try LLaMA, Mistral, etc.
    prompt = f"Explain what this Python code does:\n\n{code_str}\n\n"
    with model.chat_session():
        response = model.generate(prompt, max_tokens=300)
    return response
