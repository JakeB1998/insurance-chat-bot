from app.assistant.intent import Intent
from app.user_context import UserContext


class SessionContext():
    def __init__(self, user_ctx: UserContext = None, current_intent: Intent = None, intent_history: List[Intent] = None) -> None:
        self.user_ctx = user_ctx
        self.intent = current_intent
        self.intent_history = intent_history