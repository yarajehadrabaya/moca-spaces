import re

FORWARD_TARGET = ["2", "1", "8", "5", "4"]
BACKWARD_TARGET = ["2", "4", "7"]

WORD_TO_DIGIT = {
    "واحد": "1", "وحد": "1", "احد": "1",
    "اثنان": "2", "اثنين": "2", "اتنين": "2", "تنين": "2",
    "ثلاثة": "3", "ثلاثه": "3", "تلاتة": "3", "تلاته": "3", "تلات": "3", "ثلاث": "3",
    "اربعة": "4", "أربعة": "4", "اربعه": "4", "أربعه": "4",
    "خمسة": "5", "خمسه": "5", "خمس": "5",
    "ستة": "6", "سته": "6", "ست": "6",
    "سبعة": "7", "سبعه": "7", "سبع": "7",
    "ثمانية": "8", "ثمانيه": "8", "تمانية": "8", "تمانيه": "8", "تماني": "8", "تمنية": "8",
    "تسعة": "9", "تسعه": "9", "تسع": "9",
    "صفر": "0", "زيرو": "0"
}

def normalize_arabic(text):
    if not text: return ""
    text = text.strip().lower()
    text = re.sub("[إأآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ة", "ه", text)
    text = re.sub(r"\bو", "", text) 
    return text

def extract_digits(text):
    if not text: return []
    clean_text = normalize_arabic(text)
    

    raw_numbers = re.findall(r'\d+', clean_text)
    if raw_numbers:
        return raw_numbers

    words = clean_text.split()
    found_digits = []
    for w in words:
        if w in WORD_TO_DIGIT:
            found_digits.append(WORD_TO_DIGIT[w])
    
    return found_digits

def evaluate_forward(digits):
    return 1 if digits == FORWARD_TARGET else 0

def evaluate_backward(digits):
    return 1 if digits == BACKWARD_TARGET else 0

def evaluate_subtraction(digits):
    if not digits: return 0, 0
    correct_count = 0
    previous = 100
    nums = [int(d) for d in digits]
    
    for n in nums:
        if previous - 7 == n:
            correct_count += 1
        previous = n
    
    if correct_count >= 4: score = 3
    elif correct_count in [2, 3]: score = 2
    elif correct_count == 1: score = 1
    else: score = 0
    return correct_count, score
