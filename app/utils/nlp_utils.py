from typing import Union, Dict, List

from stanza import Document
from stanza.models.common.doc import Word

from app.assistant.nlp.nlp_context import NLPContext
from app.config.app_vars import LOGGER


def generate_document(nlp_context: NLPContext, text) -> Document:
    try:
        return nlp_context(text) if isinstance(nlp_context, NLPContext) and str(text) is not None else None
    except Exception as e:
        LOGGER.error(e, e)
        raise e



def get_subject_in_sentence(sentence, verb, translation_map: Dict[str, str]) -> Union[str, None]:
    verb = verb.lower()
    for word in sentence.words:
        # Check if word lemma matches the given verb
        if word.lemma == verb:
            governor: Word = sentence.words[word.head - 1] if word.head > 0 else word
            for w in sentence.words:
                if w.head == governor.id and w.deprel == "nsubj":
                    if translation_map is not None:
                        for before, after in translation_map.items():
                            if before.lower() == w.text.lower():
                                return after
                    return w.text
    return None


def get_subject(doc: Document, verb, translation_map: Dict[str, str]) -> Union[str, None]:
    verb = verb.lower()
    for sent in doc.sentences:
        subject = get_subject_in_sentence(sentence=sent, verb=verb, translation_map=translation_map)

        if subject is not None:
            return subject
    return None