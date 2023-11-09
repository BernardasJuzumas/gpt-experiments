#Lets make an app prototype that creates two ai agents to converse in a single thread. Agents will be able to ask each other questions and answer them.
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI()

#agent definition
conservative = client.beta.assistants.create(
    name="Conservative",
    instructions="You rigorously, yet politely defend conservative family values and tradition.",
    model="gpt-4-1106-preview"
)

liberal =  client.beta.assistants.create(
    name="Liberal",
    instructions="You rigorously, yet politely defend liberal values and exploration.",
    model="gpt-4-1106-preview"
)

#create thread
thread = client.beta.threads.create()

print("Thread id: " + thread.id)

#add message to thread
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="I'm 18 years old and about to finish the school. I'd like to take a gap year and travel around the world. My parents tell me not to waste time and go straight in to college. What do you think about that?"
)


run =  client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=conservative.id
)

print("Thread id: " + thread.id)

print(run)


