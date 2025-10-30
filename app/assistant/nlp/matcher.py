from typing import Dict, List, Any

from stanza import Document
from stanza.models.common.doc import Word, Sentence

from app.config.app_vars import LOGGER

class Match:
    def __init__(self, sentence: Sentence, starting_index: int, ending_index: int) -> None:
        self.sentence = sentence
        self.starting_index = starting_index
        self.ending_index = ending_index


class MatchedIntent(Match):
    def __init__(self, intent, sentence: list, starting_index: int, ending_index: int) -> None:
        super().__init__(sentence=sentence, starting_index=starting_index, ending_index=ending_index )
        self.intent = intent

def match_pattern_in_sentence(sentence: Sentence, pattern: List[Dict[str, str]], distance: int = 0):
    wlen = len(sentence.words)

    start_index = 0
    end_index = start_index

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

                if token_matches(sentence.words[wi + skip], p):
                    wi = wi + skip + 1  # move past the matched word
                    found = True
                    end_index = wi
                    break

            if not found:
                matched = False
                start_index = i + 1
                end_index = start_index
                break

        if matched:
            return Match(sentence, start_index, end_index)


def match_pattern(doc: Document, pattern: List[Dict[str, str]], distance: int = 0):
    """
    Returns True if the sequence of pattern tokens matches the words list,
    allowing up to `distance` non-matching words between matched tokens.
    """
    plen = len(pattern)

    for sentence in doc.sentences:
        match = match_pattern_in_sentence(sentence=sentence, pattern=pattern, distance=distance)
        if match is not None:
            return match

    return None



def get_intents(doc: Document, pattern_map: Dict[str, List[Dict[str, Any]]]) -> List[MatchedIntent]:
    # Flatten all words in the doc into a list
    intents = []

    for sentence in doc.sentences:
        for intent, pattern_ctxs in pattern_map.items():
            for pattern_ctx in pattern_ctxs:
                distance = 0

                try:
                    distance = int(pattern_ctx.get('distance', 0))
                except ValueError as e:
                    LOGGER.error(f"Failed to convert 'distance' parameter in {pattern_ctxs}. Using default distance {distance}")

                match = match_pattern_in_sentence(sentence=sentence, pattern=pattern_ctx.get('patterns', []), distance=distance)
                if isinstance(match, Match):
                    intents.append(MatchedIntent(intent=intent, sentence=sentence, starting_index=match.starting_index, ending_index=match.ending_index))
                    break

    return intents



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
