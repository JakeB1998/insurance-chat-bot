PATTERNS = [
    [{"LEMMA": "file"}, {"LEMMA": "a"}, {"LEMMA": "claim"}],
    [{"LEMMA": "report"}, {"LEMMA": "damage"}],
    [{"LEMMA": "submit"}, {"LEMMA": "claim"}]
]

PATTERNS_MAP = {
    "file_claim": [
        [{"LEMMA": "file"}, {"LEMMA": "a"}, {"LEMMA": "claim"}],
        [{"LEMMA": "report"}, {"LEMMA": "damage"}],
        [{"LEMMA": "submit"}, {"LEMMA": "claim"}],
    ],
    "get_claim": [
        [{"LEMMA": "get"}, {"LEMMA": "claim"}],
        [{"LEMMA": "check"}, {"LEMMA": "claim"}],
        [{"LEMMA": "status"}, {"LEMMA": "of"}, {"LEMMA": "claim"}],
        [{"LEMMA": "claim"}, {"LEMMA": "status"}],
        [{"LEMMA": "track"}, {"LEMMA": "claim"}],
    ],
}

class NLPConfig:
    def __init__(self, model_name: str):
        self.model_name = model_name