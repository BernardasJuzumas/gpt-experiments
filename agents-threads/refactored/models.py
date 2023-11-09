from dataclasses import dataclass
from datetime import datetime

@dataclass
class Message:
    thread_id: str
    role: str
    content: str

@dataclass
class Thread:
    id: str
    created_at: datetime
    messages: list[Message] = None

    def add_message(self, message: Message):
        if self.messages is None:
            self.messages = []
        self.messages.append(message)

@dataclass
class Assistant:
    id: str
    name: str
    model: str
    instructions: str

@dataclass
class Run:
    id: str
    thread_id: str
    assistant_id: str
    status: str