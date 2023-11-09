from openai import OpenAI
from logger import Logger

#persona maker uses opeanai api to create a persona using the given system and user prompts as strings, then outputs the persona as a sytem parameter string
class Discuss:
    def __init__(self, client=None):
        self.client = client or OpenAI()  # Allow dependency injection of the OpenAI client for testing
        self.logger = Logger(__name__)

    def discuss(self, system_prompt, user_prompt):
        try:
            self.logger.info(f"Creating response for:\nSystem prompt: {system_prompt}, \nUser prompt: {user_prompt}")
            response  = self.client.response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": User_prompt},
                ]
                )
            self.logger.info(f"\nResponse: {response}")
            return response.choices[0].text
        except Exception as e:
            self.logger.error(f"Error creating response: {e}")
            raise