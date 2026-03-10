from fastapi import FastAPI, File, UploadFile
import json, re
from cv_logic import process_clock, process_cube, process_trails
from qwen_engine import analyze_with_qwen

app = FastAPI()

def parse_res(res):
    return res.split("Analysis:")[1].strip() if "Analysis:" in res else res

@app.post("/clock")
async def clock_api(image: UploadFile = File(...)):
    res = process_clock(await image.read())
    ai_text = analyze_with_qwen("رسم الساعة", res.get("details", {}), res['score'], 3)
    return {"score": res['score'], "analysis": parse_res(ai_text), "details": res}

@app.post("/cube")
async def cube_api(image: UploadFile = File(...)):
    res = process_cube(await image.read())
    ai_text = analyze_with_qwen("نسخ المكعب", res, res['score'], 1)
    return {"score": res['score'], "analysis": parse_res(ai_text), "details": res}

@app.post("/trails")
async def trails_api(patient_file: UploadFile = File(...)):
    res = process_trails(json.load(patient_file.file))
    ai_text = analyze_with_qwen("التوصيل التتابعي", res, res['score'], 1)
    return {"score": res['score'], "analysis": parse_res(ai_text), "details": res}

@app.get("/")
def home():
    return {"status": "MoCA Vision Integrated API Final v4.5"}
