from fastapi import FastAPI, File, UploadFile
import shutil, os
from transcriber import speech_to_text
from logic import extract_digits, evaluate_forward, evaluate_backward, evaluate_subtraction
from qwen_engine import analyze_attention

app = FastAPI()

@app.post("/digits-forward")
async def digits_forward(audio: UploadFile = File(...)):
    path = f"temp_f_{audio.filename}"
    with open(path, "wb") as f: shutil.copyfileobj(audio.file, f)
    text = speech_to_text(path)
    if os.path.exists(path): os.remove(path)
    
    digits = extract_digits(text)
    score = evaluate_forward(digits)
    ai_analysis = analyze_attention("Digits Forward", text, score, 1)
    
    return {"section": "Forward", "score": int(score), "patient_said": text, "extracted_digits": digits, "analysis": ai_analysis}

@app.post("/digits-backward")
async def digits_backward(audio: UploadFile = File(...)):
    path = f"temp_b_{audio.filename}"
    with open(path, "wb") as f: shutil.copyfileobj(audio.file, f)
    text = speech_to_text(path)
    if os.path.exists(path): os.remove(path)
    
    digits = extract_digits(text)
    score = evaluate_backward(digits)
    ai_analysis = analyze_attention("Digits Backward", text, score, 1)
    
    return {"section": "Backward", "score": int(score), "patient_said": text, "extracted_digits": digits, "analysis": ai_analysis}

@app.post("/subtraction")
async def subtraction(audio: UploadFile = File(...)):
    path = f"temp_s_{audio.filename}"
    with open(path, "wb") as f: shutil.copyfileobj(audio.file, f)
    text = speech_to_text(path)
    if os.path.exists(path): os.remove(path)
    
    digits = extract_digits(text)
    count, score = evaluate_subtraction(digits)
    ai_analysis = analyze_attention("Serial 7 Subtraction", text, score, 3)
    
    return {"section": "Subtraction", "score": int(score), "correct_count": count, "patient_said": text, "extracted_digits": digits, "analysis": ai_analysis}

@app.get("/")
def home():
    return {"message": "MoCA Attention API v5.1 - Fixed Extraction Logic"}