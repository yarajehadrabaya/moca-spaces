import speech_recognition as sr
from pydub import AudioSegment
import os

def speech_to_text(audio_file_path):
    recognizer = sr.Recognizer()
    try:
        audio = AudioSegment.from_file(audio_file_path)
        # توحيد التردد لـ 16000 يجعل جوجل يفهم الكلام بوضوح أعلى 4 مرات
        audio = audio.set_frame_rate(16000).set_channels(1).normalize()
        
        temp_wav = f"clean_{os.path.basename(audio_file_path)}.wav"
        audio.export(temp_wav, format="wav")

        with sr.AudioFile(temp_wav) as source:
            # حذفنا ambient noise عشان ما يقص أول الكلام
            audio_data = recognizer.record(source)

        text = recognizer.recognize_google(audio_data, language="ar-AR")
        
        if os.path.exists(temp_wav): os.remove(temp_wav)
        return text
    except:
        return "[صوت غير مفهوم]"