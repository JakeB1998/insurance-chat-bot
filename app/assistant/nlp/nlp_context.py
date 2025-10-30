
from stanza import DownloadMethod, Pipeline

from app.assistant.nlp.nlp_config import NLPConfig


class NLPContext:
    def __init__(self, nlp_config: NLPConfig = None):
        self.nlp_config = nlp_config

        self.nlp_model = None

        if isinstance(self.nlp_config, NLPConfig):
            self.nlp_model = Pipeline(self.nlp_config.language, processors=",".join(self.nlp_config.processors),  download_method=self.nlp_config.download_method)

    def __call__(self, text: str):
        return self.nlp_model(text) if self.nlp_model is not None else None