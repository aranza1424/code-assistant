import os
from dotenv import load_dotenv
import gradio as gr
import yaml
from llm_api import LLM_API

# Cargar prompts desde archivo YAML
with open("prompts.yaml", "r") as file:
    system_prompt_dict = yaml.safe_load(file)

# Configuración inicial
load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
MODEL = os.getenv("MODEL")

# Instancia del modelo
model_llm = LLM_API(base_url=BASE_URL, api_key=API_KEY, model=MODEL)


# Función para manejar la respuesta del modelo
def response_gradio(message, history=None, topic="Docstring"):
    """
    Función que recibe el mensaje del usuario y lo envía al modelo con el prompt adecuado.
    """
    system_prompt = system_prompt_dict.get(topic, system_prompt_dict["Docstring"])
    message = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message},
    ]
    response = model_llm.get_response(message)
    return response


if __name__ == "__main__":
    with gr.Blocks() as demo:
        with gr.Row():
            with gr.Column(scale=1):
                opcion_selector = gr.Dropdown(
                    choices=list(system_prompt_dict.keys()),
                    label="Topic",
                    value="Docstring",
                )
            with gr.Column(scale=3):
                chat = gr.ChatInterface(
                    type="messages",
                    fn=response_gradio,
                    title="Python/SQL code assistant",
                    description="Generate docstrings or correct your code.",
                    theme="default",
                    additional_inputs=[opcion_selector],
                    examples=[
                        ["def add(a, b): return a + b", "Docstring"],
                        ["SELECT * FROM users WHERE id = 1", "SQL corrector"],
                        ["def add(a, b): return a + b", "Python corrector"],
                    ],
                )
    demo.launch(inbrowser=True)
