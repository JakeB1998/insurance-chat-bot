
from stanza import DownloadMethod, Pipeline

from app.assistant.nlp.nlp_config import NLPConfig


class NLPContext:
    def __init__(self, nlp_config: NLPConfig = None):
        self.nlp_config = nlp_config

        self.nlp_model = Pipeline('en', processors='tokenize,mwt,pos,lemma',  download_method=DownloadMethod.REUSE_RESOURCES)

    def __call__(self, text: str):
        return self.nlp_model(text) if self.nlp_model is not None else None