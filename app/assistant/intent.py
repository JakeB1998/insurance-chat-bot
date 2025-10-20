
class IntentTypes:
    FILE_CLAIM = "FILE_CLAIM"
    GET_CLAIM = "GET_CLAIM"
    GET_AGENT = "GET_AGENT"


class Intent:
    def __init__(self, intent_name: str):
        self.intent_name = intent_name
