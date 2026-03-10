import speech_recognition as sr
from pydub import AudioSegment
import os

def speech_to_text(audio_file_path):
    recognizer = sr.Recognizer()
    try:
        # 1. تحميل الملف ومعالجته برمجياً
        audio = AudioSegment.from_file(audio_file_path)
        
        # رفع الصوت وتوحيد التردد لضمان وضوح الكلمات القصيرة (مثل الأرقام)
        audio = audio.normalize().set_frame_rate(16000).set_channels(1)
        
        temp_wav = f"fix_{os.path.basename(audio_file_path)}.wav"
        audio.export(temp_wav, format="wav")

        with sr.AudioFile(temp_wav) as source:
            # ❌ أزلنا أي فلاتر صمت لكي لا يتم حذف الكلمات القصيرة
            audio_data = recognizer.record(source)

        # 2. محاولة التعرف على الكلام
        text = recognizer.recognize_google(audio_data, language="ar-AR")
        
        if os.path.exists(temp_wav): os.remove(temp_wav)
        return text
    except:
        # إذا فشل جوجل تماماً، نرسل نصاً فارغاً لكي يحاول الموديل تخمينه
        return "قصير المقطع الصوتي "