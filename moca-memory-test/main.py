from fastapi import FastAPI
from logic import evaluate_memory_logic

app = FastAPI()

@app.post("/memory")
async def memory_endpoint(request: dict):
    
    raw_text = request.get("words", [])

    # 1️⃣ التحليل الحتمي
    logic_res = evaluate_memory_logic(raw_text)

    # 2️⃣ تحليل LLM
    ai_res = get_memory_analysis(logic_res["matched_words"])

    # 3️⃣ استخراج السكور
    if isinstance(ai_res, int):
        final_score = ai_res
    else:
        final_score = get_score(ai_res)

    # 4️⃣ Safety Override
    if final_score == 0 and logic_res["matched_count"] > 0:
        final_score = logic_res["matched_count"]

    # 5️⃣ الإرجاع (داخل الدالة ✅)
    return {
        "score": final_score,
        "matched_words": logic_res["matched_words"]
    }