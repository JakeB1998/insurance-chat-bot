from typing import List

from stanza import DownloadMethod

from app.assistant.intent import IntentTypes



class NLPConfig:
    def __init__(self, model_name: str, language: str = "en", processors: List[str] = None, download_method: DownloadMethod = DownloadMethod.REUSE_RESOURCES):
        self.model_name = model_name
        self.language = language
        self.processors = processors
        self.download_method = download_method

        if self.processors is None:
            self.processors = []
