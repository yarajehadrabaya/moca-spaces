from fastapi import FastAPI, File, UploadFile
import shutil, os, re
from transcriber import speech_to_text
from logic import evaluate_fluency_logic
from qwen_engine import get_fluency_analysis

app = FastAPI()

@app.post("/check-fluency")
async def check_fluency(audio: UploadFile = File(...)):
    try:
        temp_input = f"input_{audio.filename}"
        with open(temp_input, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)
        
        raw_text = speech_to_text(temp_input)
        if os.path.exists(temp_input): os.remove(temp_input)
        
        logic_res = evaluate_fluency_logic(raw_text)
        
        ai_res = get_fluency_analysis(raw_text, logic_res)
        
        final_score = logic_res['score']
        analysis = ai_res.split("Analysis:")[1].strip() if "Analysis:" in ai_res else ai_res

        return {
            "question": "Fluency (Letter F)",
            "patient_said": raw_text,
            "detected_words": logic_res['words'],
            "word_count": logic_res['count'],
            "score": final_score,
            "max_score": 1,
            "doctor_analysis": analysis
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def home():
    return {"status": "Fluency API is Running"}
