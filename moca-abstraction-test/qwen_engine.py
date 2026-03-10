from huggingface_hub import InferenceClient
import os

HF_TOKEN = os.getenv("HF_TOKEN")
client = InferenceClient(api_key=HF_TOKEN)

def analyze_abstraction_pair(patient_text, pair_type):
    if pair_type == "transport":
        task_info = "وجه الشبه بين (القطار والدراجة). الإجابة الصحيحة: (وسائل مواصلات / نقل / سفر / أشياء نركبها)."
    else: # measurement
        task_info = "وجه الشبه بين (الساعة والمسطرة). الإجابة الصحيحة: (أدوات قياس / حساب الوقت والطول/ خدمات قياس  / بنقيس فيهم)."

    prompt = f"""
    أنت طبيب أعصاب خبير . قيم إجابة مريض في اختبار التجريد (Abstraction).
    المهمة: {task_info}
    المريض قال: "{patient_text}"

    قواعد التصحيح المرنة:
    1. أعط درجة (1 من 1) إذا كان المعنى يدور حول الفئة الصحيحة (مواصلات للقطار، قياس للساعة).
    2. اقبل العامية تماماً (مثل: "بنركبهم"، "وسايل"، "بنقيس"، "موازين"، "للسفر").
    3. إذا كانت الإجابة بعيدة جداً عن الوظيفة المشتركة (مثل: "لهم عجلات" أو "جماد")، أعطِ 0.
    
    رد بالتنسيق التالي حصراً:
    Score: [1 أو 0]
    Analysis: [شرح طبي رقيق ومختصر بالعربية]
    """

    try:
        response = client.chat.completions.create(
            model="Qwen/Qwen2.5-7B-Instruct",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Score: 0\nAnalysis: خطأ في الاتصال بالموديل: {str(e)}"
