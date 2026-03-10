import re
from difflib import SequenceMatcher

# معايير التسمية
NAMING_WORDS = ["أسد", "وحيد قرن", "جمل"]
STT_CONFUSION = {"خرتيت": "وحيد قرن", "فيل": "وحيد قرن", "سيد قشطة": "وحيد قرن"}

def normalize_arabic(text):
    if not text: return ""
    text = text.strip().lower()
    # توحيد الحروف
    text = re.sub("[إأآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ة", "ه", text)
    # إزالة الحروف المتكررة الناتجة عن المد (مثل ااااا)
    text = re.sub(r'(.)\1+', r'\1', text)
    # إزالة التشكيل وعلامات الترقيم
    text = re.sub(r"[\u064B-\u0652]", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    return text

def evaluate_naming_logic(text_list):
    matched = []
    for text in text_list:
        norm = normalize_arabic(text)
        for key, val in STT_CONFUSION.items():
            if key in norm: norm = val
        
        for target in NAMING_WORDS:
            if target in norm or SequenceMatcher(None, norm, target).ratio() > 0.6: # زيادة المرونة
                if target not in matched: matched.append(target)
    return matched