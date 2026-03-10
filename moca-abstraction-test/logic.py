import re

def evaluate_fluency_logic(text):
    if not text:
        return {"count": 0, "words": [], "score": 0}
    
    # تقسيم النص لكلمات وتنظيفها
    raw_words = text.split()
    detected_f_words = []
    
    for word in raw_words:
        # إزالة ال التعريف (مثلاً: الفيل تصبح فيل) لنتحقق من الحرف الأول
        clean_word = re.sub(r"^ال", "", word)
        
        # التحقق إذا كانت تبدأ بحرف الفاء
        if clean_word.startswith('ف'):
            # التأكد من عدم تكرار نفس الكلمة في العد
            if clean_word not in detected_f_words:
                detected_f_words.append(clean_word)
    
    count = len(detected_f_words)
    # قاعدة موكا: نقطة واحدة إذا ذكر 11 كلمة أو أكثر
    score = 1 if count >= 11 else 0
    
    return {
        "count": count,
        "score": score,
        "words": detected_f_words
    }