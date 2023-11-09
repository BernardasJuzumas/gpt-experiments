
"""
This module contains configuration settings for the OpenAI API key, database folder, thread message, and seed.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration Settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATABASE_FOLDER = ".cache"
THREAD_MESSAGE = "I'm 18 years old and about to finish the school. I'd like to take a gap year and travel around the world. My parents tell me not to waste time and go straight in to college. What do you think about that?"
SEED = 421

# Add more configs if needed


