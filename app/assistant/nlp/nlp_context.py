from app.assistant.nlp.nlp_config import NLPConfig


class NLPContext:
    def __init__(self, nlp_config: NLPConfig = None):
        self.nlp_config = nlp_config

        self.nlp_model = spacy.load(self.nlp_config.model_name) if self.nlp_config else None

    def __call__(self, text: str):
        return self.nlp_model(text) if self.nlp_model is not None else None