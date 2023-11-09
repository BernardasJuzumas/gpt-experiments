from openai import OpenAI
from logger import Logger
from gpt_discuss import Discuss
from config import P_PERSONA_MAKER

#persona maker uses opeanai api to create a persona using the given system and user prompts as strings, then outputs the persona as a sytem parameter string
class PersonaMaker:
    def __init__(self, client=None):
        self.client = client or OpenAI()  # Allow dependency injection of the OpenAI client for testing
        self.logger = Logger(__name__)
        self.discuss = Discuss()

    def create_persona(self, persona_prompt):
        try:
            self.logger.info(f"Creating persona for:\nPersona prompt: {persona_prompt}")
            persona  = self.discuss.discuss(P_PERSONA_MAKER, persona_prompt)
            self.logger.info(f"\nPersona: {persona}")
            return persona
        except Exception as e:
            self.logger.error(f"Error creating persona: {e}")
            raise

persona_maker = PersonaMaker().create_persona(P_PERSONA_MAKER, "Create a programmer persona as per similar example: Act as a thorough and very experienced senior programmer. Always try to assist the customer to the fullest. Write best code of your life.Your job is extremely serious: you refactor code, from trash to masterpiece. Follow all the best coding standards and practices, comment code thoroughly, make it functional and much better architected for the problems old code was trying to solve. Be very innovative yet simple with your proposed solutions.")