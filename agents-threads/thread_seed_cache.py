import os
import time
import sqlite3
import logging
from pathlib import Path
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# Constants
DATABASE_FOLDER = ".cache"
THREAD_MESSAGE = "I'm 18 years old and about to finish the school. I'd like to take a gap year and travel around the world. My parents tell me not to waste time and go straight in to college. What do you think about that?"
SEED = 69


# Database helper functions
def cache_seed(seed):
    Path(f"{DATABASE_FOLDER}/{seed}").mkdir(parents=True, exist_ok=True)


def connect_or_create_db(seed):
    cache_seed(seed)
    db_path = f"{DATABASE_FOLDER}/{seed}/log.db"
    conn = sqlite3.connect(db_path)
    conn.execute("""CREATE TABLE IF NOT EXISTS log (
                        timestamp text,
                        thread_id text,
                        run_id text,
                        assistant_id text
                    )""")
    return conn


# Conversation Manager
class ConversationManager:
    def __init__(self):
        self.client = OpenAI()  # Assume OpenAI object is correctly initialized with OPENAI_API_KEY
        self.conn = connect_or_create_db(SEED)

    def log_message(self, run):
        with self.conn as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO log VALUES (?,?,?,?)", (datetime.utcnow(), run.thread_id, run.id, run.assistant_id))
        
    def get_last_thread_and_run_id(self):
        with self.conn as connection:
            cursor = connection.cursor()
            query = cursor.execute("SELECT MAX(timestamp), thread_id, run_id FROM log GROUP BY thread_id")
            for _, thread_id, run_id in query:
                return thread_id, run_id
        return None, None

    def create_or_retrieve_thread(self, last_thread_id=None):
        if last_thread_id is None:
            thread = self.client.beta.threads.create()
            self.client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=THREAD_MESSAGE
            )
            return thread
        else:
            return self.client.beta.threads.retrieve(last_thread_id)

    def run_assistant(self, thread_id, assistant_id):
        last_run = self.get_last_run(thread_id)
        if last_run:
            while last_run.status != "completed":
                logger.info(f"Current last run status: {last_run.status}. Waiting 5 seconds.")
                time.sleep(5)
                last_run = self.client.beta.threads.runs.retrieve(run_id=last_run.id, thread_id=thread_id)

        run = self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )
        self.log_message(run)
        return run

    def get_last_run(self, thread_id):
        _, last_run_id = self.get_last_thread_and_run_id()
        if last_run_id:
            return self.client.beta.threads.runs.retrieve(run_id=last_run_id, thread_id=thread_id)
        return None

    @staticmethod
    def check_if_assistant_exists(client, name):
        matching_assistants = [assistant for assistant in client.beta.assistants.list() if assistant.name == name]
        if matching_assistants:
            return matching_assistants[0]
        else:
            return None

    def ensure_assistant_exists(self, name, instructions, model):
        assistant = self.check_if_assistant_exists(self.client, name)
        if not assistant:
            assistant = self.client.beta.assistants.create(name=name, instructions=instructions, model=model)
            logger.info(f"Created {name} assistant")
        return assistant

    def run_conversation(self):
        thread_id, _ = self.get_last_thread_and_run_id()
        thread = self.create_or_retrieve_thread(thread_id)

        conservative = self.ensure_assistant_exists("Conservative",
                                                    "You rigorously, yet politely defend conservative family values and tradition. To previous messages that challenge your beliefs respond with response and challenge of your own.",
                                                    "gpt-4-1106-preview")
        liberal = self.ensure_assistant_exists("Liberal",
                                               "You rigorously, yet politely defend liberal values, freedom of choice and exploring yourself beyond realms of traditional culture. To previous messages that challenge your beliefs respond with response and challenge of your own.",
                                               "gpt-4-1106-preview")

        self.run_assistant(thread.id, conservative.id)
        self.run_assistant(thread.id, liberal.id)

        # Returns messages for potential further processing
        return self.client.beta.threads.messages.list(thread_id=thread.id)


# Entry point for the script
if __name__ == "__main__":
    manager = ConversationManager()
    messages = manager.run_conversation()
    logger.info(messages)