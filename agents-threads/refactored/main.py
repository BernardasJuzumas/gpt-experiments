from conversation_manager import ConversationManager

def main():
    """
    Initializes the ConversationManager, runs the conversation process, closes the database connection, and outputs the messages in the conversation.
    """
    # Initialize the ConversationManager
    manager = ConversationManager()

    # Run the conversation process
    messages = manager.run_conversation()

    # Close the database connection
    manager.close()

    # Output the messages in the conversation
    for message in messages:
        print(f"{message.role}: {message.content}")
        print("*********************************************")

if __name__ == "__main__":
    main()