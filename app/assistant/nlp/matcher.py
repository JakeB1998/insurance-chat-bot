from typing import Dict, List, Any

from stanza import Document
from stanza.models.common.doc import Word

from app.config.app_vars import LOGGER


def does_pattern_match(words: List['Word'], pattern: List[Dict[str, str]], distance: int = 0):
    """
    Returns True if the sequence of pattern tokens matches the words list,
    allowing up to `distance` non-matching words between matched tokens.
    """
    plen = len(pattern)
    wlen = len(words)

    for i in range(wlen):
        # Start matching pattern from words[i]
        wi = i  # current word index
        matched = True

        for p in pattern:
            # Move forward until we find a match or exceed allowed distance
            found = False
            for skip in range(distance + 1):
                if wi + skip >= wlen:
                    matched = False
                    break
                if token_matches(words[wi + skip], p):
                    wi = wi + skip + 1  # move past the matched word
                    found = True
                    break
            if not found:
                matched = False
                break

        if matched:
            return True

    return False


def get_intent(doc: Document, pattern_map: Dict[str, List[Dict[str, Any]]]):
    # Flatten all words in the doc into a list
    words: List[Word] = [word for sent in doc.sentences for word in sent.words]

    for intent, pattern_ctxs in pattern_map.items():
        for pattern_ctx in pattern_ctxs:
            distance = 0

            try:
                distance = int(pattern_ctx.get('distance', 0))
            except ValueError as e:
                LOGGER.error(f"Failed to convert 'distance' parameter in {pattern_ctxs}. Using default distance {distance}")

            if does_pattern_match(words, pattern_ctx.get('patterns', []), distance=distance):
                return intent


def token_matches(stanza_word: Word, pattern_token: Dict[str, str]):
    for attr, value in pattern_token.items():
        # Get attribute from stanza Word object
        # attr is the stanza augment located in the patterns configuration
        # value is a string value of the word
        token_value = getattr(stanza_word, attr.lower(), None)
        if token_value is None:
            return False
        if token_value.lower() != value.lower():
            return False
    return True
