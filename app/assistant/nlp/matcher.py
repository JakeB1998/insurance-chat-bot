from typing import Dict, List

from stanza import Document
from stanza.models.common.doc import Word


def does_pattern_match(words: List[Word], pattern: List[Dict[str, str]]):
    # pattern: List[dict]
    plen = len(pattern)
    # How many words in the pattern
    for i in range(len(words) - plen + 1):
        # Gets a window of words the size of the pattern that slides.
        window: list = words[i:i+plen]

        # Zip matches each stanza word object to each word instance in the pattern
        # Then iterates the pairs passing them to check if they equal eachother.
        if all(token_matches(w, pt) for w, pt in zip(window, pattern)):
            return True
    return False

def match_patterns(doc: Document, patterns: List[List[Dict[str, str]]]):
    matches = []
    # Flatten all words in the doc into a list
    words: List[Word] = [word for sent in doc.sentences for word in sent.words]

    for pattern in patterns:
        # Pattern is a list of kew pair values (key: stanza augment, value: word to look for)
        plen = len(pattern)
        for i in range(len(words) - plen + 1):
            # Gets a window of words the size of the pattern that slides.
            window: list = words[i:i+plen]

            # Zip matches each stanza word object to each word instance in the pattern
            # Then iterates the pairs passing them to check if they equal eachother.
            if all(token_matches(w, pt) for w, pt in zip(window, pattern)):
                matched_text = " ".join(w.text for w in window)
                matches.append((matched_text, i, i+plen))
    return matches

def get_intent(doc, pattern_map: Dict[str, List[List[Dict[str, str]]]]):
    # Flatten all words in the doc into a list
    words: List[Word] = [word for sent in doc.sentences for word in sent.words]

    for intent, patterns in pattern_map.items():
        for pattern in patterns:
            # Pattern is a list of kew pair values (key: stanza augment, value: word to look for)
            if does_pattern_match(words, pattern):
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
