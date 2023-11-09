from openai import OpenAI

from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI()

#delete = client.beta.threads.delete("thread_4Dr1KplohnLs4pJC9X1VvanA")