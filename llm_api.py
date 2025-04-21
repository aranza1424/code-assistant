from openai import OpenAI


class LLM_API:
    """
    Clase para interactuar con un modelo de lenguaje a través de la API de OpenAI-compatible.

    Atributos:
        base_url (str): URL base de la API.
        api_key (str): Clave de API.
        model (str): Nombre del modelo a utilizar.
        parameters (dict): Parámetros opcionales para el modelo.
    """

    def __init__(self, base_url, api_key, model="qwen2.5-coder:7b", parameters=None):
        self.base_url = base_url
        self.api_key = api_key
        self.model = model
        self.response = None
        self.parameters = parameters if parameters else {}

    def get_response(self, message):
        """
        Envía un mensaje al modelo y devuelve la respuesta generada.

        Args:
            message (list): Lista de diccionarios con claves 'role' y 'content'.

        Returns:
            str: Respuesta generada por el modelo.
        """
        try:
            client = OpenAI(api_key=self.api_key, base_url=self.base_url)
            response = client.chat.completions.create(
                model=self.model, messages=message, **self.parameters
            )
            self.response = response.choices[0].message.content
            return self.response

        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"
