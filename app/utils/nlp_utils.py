from app.assistant.nlp.nlp_context import NLPContext


def get_intent(text, nlp_ctx: NLPContext) -> str:
    if nlp_ctx is not None:
        return nlp_ctx(text)

    return None