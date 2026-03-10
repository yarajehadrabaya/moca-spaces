from difflib import SequenceMatcher

MEMORY_WORDS = ["راس", "مخمل", "برج", "ورد", "بني"]

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def is_valid_match(spoken, target):
    if spoken == target:
        return True
    
    sim = similarity(spoken, target)
    length_ok = abs(len(spoken) - len(target)) <= 1
    
    if sim >= 0.85 and length_ok:
        return True
    
    return False


def evaluate_memory_logic(spoken_words):
    matched_targets = set()
    
    for word in spoken_words:
        for target in MEMORY_WORDS:
            if target in matched_targets:
                continue
            
            if is_valid_match(word, target):
                matched_targets.add(target)
                break
    
    return {
        "score": len(matched_targets),
        "matched_count": len(matched_targets),
        "matched_words": list(matched_targets)
    }