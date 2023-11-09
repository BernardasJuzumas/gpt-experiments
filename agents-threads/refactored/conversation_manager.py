

"""
This module contains the ConversationManager class, which is responsible for managing conversations between users and assistants.
It uses the OpenAI API to create and manage threads, runs, and messages, and to retrieve and cache assistant information.
The ConversationManager class also logs runs to a database using the DBManager class.
"""
from datetime import datetime
from db_manager import DBManager
import config
from models import Thread, Run, Message
from assistant_manager import AssistantManager
from openai import OpenAI
from time import sleep

class ConversationManager:
    """
    A class that manages conversations between users and OpenAI assistants.
    It provides methods to retrieve messages from a thread, create or retrieve a thread, run an assistant, and log runs.
    """
    
    def __init__(self):
        self.db_manager = DBManager(config.SEED)
        self.assistant_manager = AssistantManager() 
        self.client = OpenAI()  # Assume OpenAI object is correctly initialized


    def get_thread_messages(self, thread_id):
            """
            Retrieves all messages in a given thread and returns them as a list of Message objects.

            Args:
                thread_id (str): The ID of the thread to retrieve messages from.

            Returns:
                list: A list of Message objects representing the messages in the thread.
            """
            messages_data = self.client.beta.threads.messages.list(thread_id=thread_id, order="asc")
            messages = []
            assistant_cache = {}  # Cache assistant information to avoid repeated API calls

            for thread_message in messages_data:
                assistant_name = "User"
                assistant_id = thread_message.assistant_id
                
                if assistant_id:
                    if assistant_id not in assistant_cache:
                        # Retrieve assistant information just once and cache it
                        assistant = self.client.beta.assistants.retrieve(assistant_id=assistant_id)
                        assistant_cache[assistant_id] = assistant.name
                    
                    assistant_name = assistant_cache[assistant_id]

                # Construct the Message model
                content = thread_message.content[0].text.value
                message = Message(
                    thread_id=thread_id,
                    role=assistant_name,
                    content=content
                )
                messages.append(message)
            return messages

    def log_run(self, run: Run):
        
        self.db_manager.execute("""
            INSERT INTO log (timestamp, thread_id, run_id, assistant_id)
            VALUES (?, ?, ?, ?)
        """, (datetime.utcnow(), run.thread_id, run.id, run.assistant_id))

    def retrieve_last_run(self, thread_id):
        
        result = self.db_manager.execute("""
            SELECT run_id FROM log WHERE thread_id = ? ORDER BY timestamp DESC LIMIT 1
        """, (thread_id,))
        if result:
            return Run(id=result[0][0], thread_id=thread_id, assistant_id=None, status=None)
        return None
    
    def create_or_retrieve_thread(self, last_thread_id=None):
        if last_thread_id is None:
            thread_data = self.client.beta.threads.create()
            thread = Thread(id=thread_data.id, created_at=datetime.utcnow())
            message = Message(thread_id=thread.id, role="user", content=config.THREAD_MESSAGE)
            self.client.beta.threads.messages.create(thread_id=thread.id, role=message.role, content=message.content)
            return thread
        else:
            thread_data = self.client.beta.threads.retrieve(last_thread_id)
            return Thread(id=thread_data.id, created_at=datetime.fromisoformat(thread_data.created_at))

    # More methods ...

    def close(self):
        self.db_manager.close()


    def run_conversation(self):
        # Retrieve or create the last thread
          # Retrieve or create the last thread
        thread_id, _ = self.db_manager.get_last_thread_and_run_id()
        thread = self.create_or_retrieve_thread(thread_id)

        # Ensure the existence of the two personas using the AssistantManager's new method
        conservative_instructions = (
            "You rigorously, yet politely defend conservative family values and tradition. "
            "To previous messages that challenge your beliefs respond with response and challenge of your own."
        )
        liberal_instructions = (
            "You rigorously, yet politely defend liberal values, freedom of choice and exploring yourself "
            "beyond realms of traditional culture. To previous messages that challenge your beliefs respond "
            "with response and challenge of your own."
        )

        conservative = self.assistant_manager.get_or_create_assistant(
            "Conservative", "gpt-4-1106-preview", conservative_instructions
        )
        liberal = self.assistant_manager.get_or_create_assistant(
            "Liberal", "gpt-4-1106-preview", liberal_instructions
        )
        
        # Run the conversation with both assistants
        conserv_run = self.run_assistant(thread.id, conservative.id)
        liberal_run = self.run_assistant(thread.id, liberal.id)


        messages = self.get_thread_messages(thread.id)
        
        # ... rest of run_conversation logic
        # Instead of returning messages, you could also print them here or handle them as needed.
        return messages
    
    def wait_for_run_completion(self, run: Run):
        """Waits for the run to complete by periodically checking its status."""
        while True:
            current_run = self.client.beta.threads.runs.retrieve(run_id=run.id, thread_id=run.thread_id)
            
            if current_run.status == 'completed':
                return current_run
            elif current_run.status == 'failed':
                raise Exception(f"Run with ID {run.id} has failed.")
            
            sleep(5)  # Wait for 5 seconds before re-checking the status

    def run_assistant(self, thread_id, assistant_id):
        """Starts a new run or continues an existing one with the assistant."""
         # Retrieve the last run and wait for it to complete before starting a new one
        last_run = self.retrieve_last_run(thread_id)
        if last_run is not None:
            self.wait_for_run_completion(last_run)

        # Start a new run
        new_run_data = self.client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id)
        new_run = Run(id=new_run_data.id, thread_id=thread_id, assistant_id=assistant_id, status=new_run_data.status)
        
        # Log newly created run
        self.log_run(new_run)
        
        # Wait for the new run to complete
        completed_run = self.wait_for_run_completion(new_run)

        return completed_run
    def create_or_retrieve_thread(self, last_thread_id=None):
        if last_thread_id is None:
            thread_data = self.client.beta.threads.create()
            thread = Thread(id=thread_data.id, created_at=datetime.utcnow())
            self.client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=config.THREAD_MESSAGE  # Make sure THREAD_MESSAGE is imported from config.py
            )
            return thread
        else:
            thread_data = self.client.beta.threads.retrieve(last_thread_id)
            # We assume the response includes a 'created_at' or similar timestamp field.
            # Use the accurate field name based on the actual API response structure.
            return Thread(
                id=thread_data.id,
                created_at=datetime.fromtimestamp(thread_data.created_at),
                messages=[]  # Assuming threads have an associated list of messages.
            )


# ... rest of the code