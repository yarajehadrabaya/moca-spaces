from fastapi import FastAPI, File, UploadFile
import shutil, os, re
from transcriber import speech_to_text
from qwen_engine import analyze_abstraction_pair

app = FastAPI()

def parse_ai_result(text):
    score = 1 if "Score: 1" in text else 0
    # استخراج التحليل بعد كلمة Analysis: أو إرجاع النص كاملاً إذا لم توجد
    analysis = text.split("Analysis:")[1].strip() if "Analysis:" in text else text
    return score, analysis

@app.post("/pair1-transport")
async def check_transport(audio: UploadFile = File(...)):
    path = f"temp_p1_{audio.filename}"
    with open(path, "wb") as f: shutil.copyfileobj(audio.file, f)
    text = speech_to_text(path)
    if os.path.exists(path): os.remove(path)
    
    # معالجة حالة عدم وجود صوت أو صوت غير مفهوم
    if not text or text.strip() == "":
        return {
            "question": "Abstraction: Train-Bicycle",
            "score": 0,
            "max_score": 1,
            "patient_said": "[صوت غير مسموع أو غير مفهوم]",
            "doctor_analysis": "لم يتمكن النظام من التعرف على إجابة واضحة من المريض، لذا تم احتساب الدرجة صفر."
        }
    
    raw_res = analyze_abstraction_pair(text, "transport")
    score, analysis = parse_ai_result(raw_res)
    
    return {
        "question": "Abstraction: Train-Bicycle",
        "score": score,
        "max_score": 1,
        "patient_said": text,
        "doctor_analysis": analysis
    }

@app.post("/pair2-measurement")
async def check_measurement(audio: UploadFile = File(...)):
    path = f"temp_p2_{audio.filename}"
    with open(path, "wb") as f: shutil.copyfileobj(audio.file, f)
    text = speech_to_text(path)
    if os.path.exists(path): os.remove(path)
    
    # معالجة حالة عدم وجود صوت أو صوت غير مفهوم
    if not text or text.strip() == "":
        return {
            "question": "Abstraction: Watch-Ruler",
            "score": 0,
            "max_score": 1,
            "patient_said": "[صوت غير مسموع أو غير مفهوم]",
            "doctor_analysis": "لم يتمكن النظام من التعرف على إجابة واضحة من المريض، لذا تم احتساب الدرجة صفر."
        }
    
    raw_res = analyze_abstraction_pair(text, "measurement")
    score, analysis = parse_ai_result(raw_res)
    
    return {
        "question": "Abstraction: Watch-Ruler",
        "score": score,
        "max_score": 1,
        "patient_said": text,
        "doctor_analysis": analysis
    }

@app.get("/")
def home():
    return {"status": "Abstraction API with Silence Handling is Running"}