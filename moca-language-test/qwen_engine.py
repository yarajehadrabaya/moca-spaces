from huggingface_hub import InferenceClient
import os

HF_TOKEN = os.getenv("HF_TOKEN")
client = InferenceClient(api_key=HF_TOKEN)

def ask_qwen(prompt):
    try:
        response = client.chat.completions.create(
            model="Qwen/Qwen2.5-7B-Instruct",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Score: 0\nAnalysis: خطأ في الاتصال: {str(e)}"

def analyze_naming(combined_text):
    prompt = f"""
    أنت طبيب أعصاب خبير. المريض طُلب منه تسمية: (أسد، وحيد قرن، جمل).
    النص المستخرج: "{combined_text}"
    المطلوب:
    - كن رحيماً جداً مع أخطاء النطق أو التشويش (مثل "اسيد" بدل "اسد" أو "جميل" بدل "جمل").
    - إذا كان المعنى واضحاً، أعطِ الدرجة.
    رد حصراً بهذا التنسيق:
    Score: [الرقم]
    Analysis: [التحليل الطبي بالعربي]
    """
    return ask_qwen(prompt)

def analyze_sentence(patient_said, target, sentence_num):
    prompt = f"""
    أنت طبيب أعصاب متخصص. المريض طُلب منه إعادة هذه الجملة: "{target}"
    المريض قال فعلياً: "{patient_said}"
    
    ⚠️ قواعد الرحمة الطبية:
    1. تجاهل تماماً أخطاء الـ STT الصوتية (مثل "ان" بدل "انا" أو "الهير" بدل "الهر").
    2. إذا كانت الكلمات الأساسية موجودة والجملة حافظت على هيكلها، الدرجة (1).
    3. لا تحسم درجة على مد الحروف أو التلعثم البسيط.
    4. امنح (0) فقط إذا غيّر المريض معنى الجملة تماماً أو سكت.

    رد حصراً بالتنسيق التالي:
    Score: [1 أو 0]
    Analysis: [شرح طبي رقيق لسبب الدرجة بالعربي]
    """
    return ask_qwen(prompt)