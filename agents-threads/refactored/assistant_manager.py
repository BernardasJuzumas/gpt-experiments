from openai import OpenAI
from models import Assistant
from logger import Logger

class AssistantManager:
    def __init__(self, client=None):
        self.client = client or OpenAI()  # Allow dependency injection of the OpenAI client for testing
        self.logger = Logger(__name__)

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
                self.logger.info(f"Assistant found: {name}")
                data = matching_assistants[0]
                return Assistant(
                    id=data.id,
                    name=data.name,
                    model=data.model,  # API response may not include model
                    instructions=data.instructions  # API response may not include instructions
                )
            self.logger.info(f"Assistant NOT found: {name}")
            return None

    def create_assistant(self, name, model, instructions):
        try:
            assistant_data = self.client.beta.assistants.create(name=name, model=model, instructions=instructions)
            self.logger.info(f"Assistant created: {name}")
            return Assistant(
                id=assistant_data.id,
                name=assistant_data.name,
                model=assistant_data.model,  # API response may not include model
                instructions=assistant_data.instructions  # API response may not include instructions
            )
        except Exception as e:
            self.logger.error(f"Error creating assistant: {e}")
            raise

    def get_or_create_assistant(self, name, model, instructions):
        try:
            assistant = self.check_if_assistant_exists(name)
            if assistant is None:
                assistant = self.create_assistant(name, model, instructions)
            self.logger.info(f"Assistant added \nName: {name}; \nmodel: {model}; \ninstructions: {instructions}")
            return assistant
        except Exception as e:
            self.logger.error(f"Error getting or creating assistant: {e}")
            raise