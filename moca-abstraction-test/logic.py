import re

def evaluate_fluency_logic(text):
    if not text:
        return {"count": 0, "words": [], "score": 0}
    
    raw_words = text.split()
    detected_f_words = []
    
    for word in raw_words:
        clean_word = re.sub(r"^ال", "", word)
        
        if clean_word.startswith('ف'):
            if clean_word not in detected_f_words:
                detected_f_words.append(clean_word)
    
    count = len(detected_f_words)
    score = 1 if count >= 11 else 0
    
    return {
        "count": count,
        "score": score,
        "words": detected_f_words
    }
