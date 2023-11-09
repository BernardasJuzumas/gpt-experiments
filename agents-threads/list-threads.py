from openai import OpenAI

from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI()

thread = client.beta.threads.retrieve("thread_YWb6fXcvE9frvYBDkerDJwbm")
messages = client.beta.threads.messages.list("thread_YWb6fXcvE9frvYBDkerDJwbm")
threads = client.beta.threads

print(threads)

