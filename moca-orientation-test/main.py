from fastapi import FastAPI, File, UploadFile, Form
import shutil, os, re
from transcriber import speech_to_text
from qwen_engine import analyze_orientation

app = FastAPI()

def parse_res(text):
    score = 0
    match = re.search(r"Score:\s*\[?(\d+)\]?", text)
    if match: score = int(match.group(1))
    analysis = text.split("Analysis:")[1].strip() if "Analysis:" in text else text
    return score, analysis

@app.post("/check-orientation")
async def check_orientation(
    expected_place: str = Form(...),
    expected_city: str = Form(...),
    audio_weekday: UploadFile = File(...),
    audio_month: UploadFile = File(...),
    audio_year: UploadFile = File(...),
    audio_place: UploadFile = File(...),
    audio_city: UploadFile = File(...)
):
    audios = {
        "يوم الأسبوع": audio_weekday,
        "الشهر": audio_month,
        "السنة": audio_year,
        "المكان": audio_place,
        "المدينة": audio_city
    }
    
    combined_transcription = ""
    
    for label, audio_file in audios.items():
        path = f"temp_{label}_{audio_file.filename}"
        with open(path, "wb") as buffer:
            shutil.copyfileobj(audio_file.file, buffer)
        
        text = speech_to_text(path)
        if os.path.exists(path): os.remove(path)
        
        combined_transcription += f"- {label}: {text if text else '[صوت غير واضح]'}\n"

    # نرسل النصوص المجمعة للتحليل الذكي
    raw_res = analyze_orientation(combined_transcription, expected_place, expected_city)
    score, analysis = parse_res(raw_res)
    
    return {
        "question": "Orientation (5 Points)",
        "score": score,
        "max_score": 5,
        "transcriptions": combined_transcription,
        "doctor_analysis": analysis
    }

@app.get("/")
def home():
    return {"status": "Orientation API v6.0 - Dialect & Numeric Month Support Active"}