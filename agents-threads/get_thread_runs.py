from openai import OpenAI

from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI()


thread_id = "thread_5UNMS8sydjWsaELVIHImZ3oN"

thread_runs = client.beta.threads.runs.list(thread_id)

for thread_run in thread_runs:
    print("Thread run: "+thread_run.id+"; Status: "+thread_run.status)
    thread_runs = client.beta.threads.runs.steps.list(thread_id=thread_id, run_id=thread_run.id)

    for thread_run_step in thread_runs:
        print("Step: "+thread_run_step.id+"; Status: "+thread_run_step.status)


