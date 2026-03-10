from fastapi import FastAPI, File, UploadFile
from typing import List
import shutil, os, re
from transcriber import speech_to_text
from qwen_engine import analyze_naming, analyze_sentence

app = FastAPI()

def get_score(text):
    # بحث متطور عن الرقم داخل الأقواس أو بجانب كلمة Score
    match = re.search(r"Score:\s*\[?(\d+)\]?", text)
    if match:
        return int(match.group(1))
    # محاولة أخيرة إذا كتب الموديل الرقم فقط في البداية
    first_digit = re.search(r"(\d)", text)
    return int(first_digit.group(1)) if first_digit else 0

@app.post("/naming")
async def check_naming(audios: List[UploadFile] = File(...)):
    texts = []
    for audio in audios:
        path = f"temp_{audio.filename}"
        with open(path, "wb") as f: shutil.copyfileobj(audio.file, f)
        transcription = speech_to_text(path)
        texts.append(transcription)
        os.remove(path)
    
    combined = " ، ".join(texts)
    ai_res = analyze_naming(combined)
    final_score = get_score(ai_res)
    return {"question": "Naming", "score": final_score, "analysis": ai_res, "patient_said": texts}

@app.post("/sentence1")
async def sentence1(audio: UploadFile = File(...)):
    path = "temp_s1.wav"
    with open(path, "wb") as f: shutil.copyfileobj(audio.file, f)
    text = speech_to_text(path)
    os.remove(path)
    
    ai_res = analyze_sentence(text, "أنا أعلم فقط أن باسل هو من يعمل اليوم", 1)
    final_score = get_score(ai_res)
    return {"question": "Sentence 1", "score": final_score, "analysis": ai_res, "patient_said": text}

@app.post("/sentence2")
async def sentence2(audio: UploadFile = File(...)):
    path = "temp_s2.wav"
    with open(path, "wb") as f: shutil.copyfileobj(audio.file, f)
    text = speech_to_text(path)
    os.remove(path)
    
    ai_res = analyze_sentence(text, "الهر يختبئ دائما تحت المقعد عندما يدخل الكلب الغرفة", 2)
    final_score = get_score(ai_res)
    return {"question": "Sentence 2", "score": final_score, "analysis": ai_res, "patient_said": text}

@app.get("/")
def home():
    return {"message": "MoCA Language API v5.0 - Compassionate Evaluation Active"}