def token_matches(stanza_word, pattern_token):
    for attr, value in pattern_token.items():
        # Get attribute from stanza Word object
        token_value = getattr(stanza_word, attr.lower(), None)
        if token_value is None:
            return False
        if token_value.lower() != value.lower():
            return False
    return True



def match_patterns(doc, patterns):
    matches = []
    # Flatten all words in the doc into a list
    words = [word for sent in doc.sentences for word in sent.words]

    for pattern in patterns:
        plen = len(pattern)
        for i in range(len(words) - plen + 1):
            window = words[i:i+plen]
            if all(token_matches(w, pt) for w, pt in zip(window, pattern)):
                matched_text = " ".join(w.text for w in window)
                matches.append((matched_text, i, i+plen))
    return matches

def get_intent(doc, pattern_map):
    # Flatten all words in the doc into a list
    words = [word for sent in doc.sentences for word in sent.words]

    for intent, patterns in pattern_map.items():
        for pattern in patterns:
            plen = len(pattern)
            for i in range(len(words) - plen + 1):
                window = words[i:i+plen]
                if all(token_matches(w, pt) for w, pt in zip(window, pattern)):
                    return intent
