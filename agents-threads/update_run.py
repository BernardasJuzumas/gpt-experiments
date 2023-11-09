from datetime import datetime
import time
from openai import OpenAI
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SEED = 42
THREAD_MESSAGE = "I'm 18 years old and about to finish the school. I'd like to take a gap year and travel around the world. My parents tell me not to waste time and go straight in to college. What do you think about that?"

client = OpenAI()

#connect or create sqlite database in .cache/SEED/log.db
def cache_seed(seed):
    if not os.path.exists(".cache"):
        os.mkdir(".cache")
    if not os.path.exists(f".cache/{seed}"):
        os.mkdir(f".cache/{seed}")
    


def connect_or_create_db(seed):
    cache_seed(seed)
    if os.path.exists(f".cache/{seed}/log.db"):
        return sqlite3.connect(f".cache/{seed}/log.db")
    else:
        conn = sqlite3.connect(f".cache/{seed}/log.db")
        c = conn.cursor()
        # Create table if it does not exist log: timestamp, thread_id, run_id, assistant_id, message
        c.execute("""CREATE TABLE IF NOT EXISTS log (
            timestamp text,
            thread_id text,
            run_id text,
            assistant_id text
        )""")
        return sqlite3.connect(f".cache/{seed}/log.db")

conn = connect_or_create_db(SEED)

def log_message(run):
    c = conn.cursor()
    c.execute("INSERT INTO log VALUES (?,?,?,?)", (datetime.now(), run.thread_id, run.id, run.assistant_id))
    conn.commit()
    
def get_last_thread_and_run_id():  
    c = conn.cursor()
    cached_thread_count = c.execute("SELECT COUNT(DISTINCT thread_id) FROM log").fetchone()[0]
    if cached_thread_count > 0:
        ltid = c.execute("SELECT thread_id FROM log ORDER BY timestamp DESC LIMIT 1").fetchone()[0]
        rid = c.execute("SELECT run_id FROM log ORDER BY timestamp DESC LIMIT 1").fetchone()[0]
        #return thread id from last row
        return ltid, rid
    else:
        return None, None
    

last_thread_id, last_run_id = get_last_thread_and_run_id()

print("**Last thread id: "+str(last_thread_id)+"**")
print("**Last run id: "+str(last_run_id)+"**")

thread = None
if last_thread_id is None:
    thread = client.beta.threads.create()
    last_thread_id = thread.id
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=THREAD_MESSAGE
    )
else:
    thread = client.beta.threads.retrieve(last_thread_id)

LAST_RUN = None

# This assumes you have `last_run_id` and `last_thread_id` defined or passed them here
if last_run_id and last_thread_id:
    LAST_RUN = client.beta.threads.runs.retrieve(run_id=last_run_id, thread_id=last_thread_id)
    print("**Last run status: " + LAST_RUN.status + "**")
else:
    print("**No last run**")

def run_assistant(thread_id, assistant_id):
    global LAST_RUN # Declare LAST_RUN as global if you're going to modify it
    lr = LAST_RUN # Use lr as local version of LAST_RUN, which reflects the current last run

    if lr is not None:
        while lr.status != "completed":
            # Wait 5 seconds
            print("**Last run status: " + lr.status + " Waiting 5 seconds to change**")
            time.sleep(5)
            lr = client.beta.threads.runs.retrieve(run_id=lr.id, thread_id=thread_id)
        print("**Last runs " + lr.id + ", status: " + lr.status + "**")
    else:
        print("**No last run**")

    print("**Creating new run for assistant: " + assistant_id + "**")
    lr = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

    print("**Created run " + lr.id + " for assistant: " + assistant_id + "**")
    log_message(lr)
    LAST_RUN = lr # Update the global LAST_RUN
    return lr

def check_if_assistant_exists(name):
    assistants = client.beta.assistants.list()
    for assistant in assistants:
        if assistant.name == name:
            print("**Assistant "+name+" exists**")  
            return assistant 
    print("**Assistant "+name+" does not exist**")
    return None

conservative = check_if_assistant_exists("Conservative")
if conservative is None:
    conservative = client.beta.assistants.create(
        name="Conservative",
        instructions="You rigorously, yet politely defend conservative family values and tradition. To previous messages that challenge your beliefs respond with response and challenge of your own.",
        model="gpt-4-1106-preview"
    )
    print("**Created Conservative assistant**")

liberal = check_if_assistant_exists("Liberal")
if liberal is None:
    liberal = client.beta.assistants.create(
        name="Liberal",
        instructions="You rigorously, yet politely defend liberal values, freedom of choice and exploring yourself beyond realms of traditional culture. To previous messages that challenge your beliefs respond with response and challenge of your own.",
        model="gpt-4-1106-preview"
    )
    print("**Created Liberal assistant**")


run_assistant(thread.id, conservative.id)
run_assistant(thread.id, liberal.id)

print(str(client.beta.threads.messages.list(thread_id=thread.id)))