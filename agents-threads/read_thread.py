from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
THREAD_ID = "thread_4Dr1KplohnLs4pJC9X1VvanA"

client = OpenAI()

threads = client.beta.threads.retrieve()
print(threads)
thread_messages = client.beta.threads.messages.list(thread_id=THREAD_ID, order="asc")


for thread_message in thread_messages:
    assistant_name = "User"
    assistant_id = thread_message.assistant_id
    if assistant_id is not None:
        assistant = client.beta.assistants.retrieve(assistant_id=assistant_id)
        assistant_name = assistant.name


    print("*****************************************************")
    print("Assistant: " + str(assistant_name))
    print("Response: " + str(thread_message.content[0].text.value))
    print("*****************************************************")

# good threads:
# thread_5N8O54clVDcEmWtyFHe8sD9X