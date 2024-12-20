from fuzzywuzzy import fuzz, process

def fuzzy_match(pattern, narration, threshold=75):
    words = narration.split('/')
    best_match, similarity = process.extractOne(pattern, words, scorer=fuzz.partial_ratio)
    if similarity >= threshold:
        return best_match, similarity
    else:
        return None, 0
    
