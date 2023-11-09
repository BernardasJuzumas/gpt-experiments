from openai import OpenAI
from models import Assistant

class AssistantManager:
    def __init__(self, client=None):
        self.client = client or OpenAI()  # Allow dependency injection of the OpenAI client for testing

    def check_if_assistant_exists(self, name):
            """
            Check if an assistant with the given name exists in the OpenAI API.

            Args:
                name (str): The name of the assistant to check.

            Returns:
                Assistant or None: If an assistant with the given name exists, return an Assistant object
                representing the assistant. Otherwise, return None.
            """
            matching_assistants = [
                assistant for assistant in self.client.beta.assistants.list() 
                if assistant.name == name
            ]
            if matching_assistants:
                data = matching_assistants[0]
                return Assistant(
                    id=data.id,
                    name=data.name,
                    model=data.model,  # API response may not include model
                    instructions=data.instructions  # API response may not include instructions
                )
            return None

    def create_assistant(self, name, model, instructions):
        assistant_data = self.client.beta.assistants.create(name=name, model=model, instructions=instructions)
        return Assistant(
            id=assistant_data.id,
            name=assistant_data.name,
            model=assistant_data.model,  # API response may not include model
            instructions=assistant_data.instructions  # API response may not include instructions
        )

    def get_or_create_assistant(self, name, model, instructions):
        assistant = self.check_if_assistant_exists(name)
        if assistant is None:
            assistant = self.create_assistant(name, model, instructions)
        return assistant