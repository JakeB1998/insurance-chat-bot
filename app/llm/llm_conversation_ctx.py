from typing import List, Dict


class LLMConversationCTX:
    """
    Maintains the context of a conversation as a history of message exchanges.

    Each message in the conversation history is represented as a dictionary with
    keys 'assistant' and 'user', storing their respective message texts.

    Attributes:
        conversation_history (List[Dict]): A list of dictionaries representing the
            conversation history. Each dictionary should have keys:
            - 'assistant': The assistant's message as a string.
            - 'user': The user's message as a string.

    Args:
        conversation_history (List[Dict]): Initial conversation history. If None,
            initializes to an empty list.
    """
    def __init__(self, conversation_history: List[Dict] = None, max_entries: int = 25):
        self.conversation_history = conversation_history
        self.max_entries = 25

        if self.conversation_history is None:
            self.conversation_history = []

    def add(self, question, response):
        if self.conversation_history is None:
            self.conversation_history = []

        if len(self.conversation_history) >= self.max_entries:
            self.conversation_history.pop(0)

        self.conversation_history.append({"user": question, "assistant": response})