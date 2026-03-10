import speech_recognition as sr
from pydub import AudioSegment
import os

def speech_to_text(audio_file_path):
    recognizer = sr.Recognizer()
    try:
        # 1. تحويل الملف وتوحيد التردد لـ 16000 وقناة واحدة (Mono)
        audio = AudioSegment.from_file(audio_file_path)
        audio = audio.set_frame_rate(16000).set_channels(1).normalize()
        
        temp_wav = f"clean_{os.path.basename(audio_file_path)}.wav"
        audio.export(temp_wav, format="wav")

        with sr.AudioFile(temp_wav) as source:
            # قراءة المقطع كاملاً بدون فترات صمت معايرة
            audio_data = recognizer.record(source)

        # 2. التعرف على الكلام (بالعربية)
        text = recognizer.recognize_google(audio_data, language="ar-AR")
        
        if os.path.exists(temp_wav): os.remove(temp_wav)
        return text
    except:
        return "[صوت غير مفهوم]"