from app.assistant.intent import IntentTypes

PATTERNS = [
    [{"LEMMA": "file"}, {"LEMMA": "a"}, {"LEMMA": "claim"}],
    [{"LEMMA": "report"}, {"LEMMA": "damage"}],
    [{"LEMMA": "submit"}, {"LEMMA": "claim"}]
]

PATTERNS_MAP = {
    IntentTypes.FILE_CLAIM: [
        [{"LEMMA": "file"}, {"LEMMA": "a"}, {"LEMMA": "claim"}],
        [{"LEMMA": "report"}, {"LEMMA": "damage"}],
        [{"LEMMA": "submit"}, {"LEMMA": "claim"}],
        [{"LEMMA": "file"}, {"LEMMA": "claim"}],
    ],
    IntentTypes.GET_CLAIM: [
        [{"LEMMA": "get"}, {"LEMMA": "claim"}],
        [{"LEMMA": "check"}, {"LEMMA": "claim"}],
        [{"LEMMA": "status"}, {"LEMMA": "of"}, {"LEMMA": "claim"}],
        [{"LEMMA": "claim"}, {"LEMMA": "status"}],
        [{"LEMMA": "track"}, {"LEMMA": "claim"}],
    ],
    IntentTypes.GET_AGENT: [
        [{"LEMMA": "get"}, {"LEMMA": "agent"}], ]
}

class NLPConfig:
    def __init__(self, model_name: str):
        self.model_name = model_name