from huggingface_hub import InferenceClient
import os

HF_TOKEN = os.getenv("HF_TOKEN")
client = InferenceClient(api_key=HF_TOKEN)

def get_fluency_analysis(text, logic_res):
    prompt = f"""
    أنت طبيب أعصاب تصحح اختبار موكا (طلاقة الكلام - حرف الفاء).
    المريض طُلب منه ذكر كلمات تبدأ بحرف الفاء في دقيقة واحدة.
    النص المستخرج من صوته: "{text}"
    الكلمات التي تم عدها برمجياً: {logic_res['words']}
    العدد الإجمالي: {logic_res['count']} (المطلوب للنجاح 11 كلمة أو أكثر).

    المطلوب:
    1. راجع النص، هل هناك كلمات تبدأ بالفاء لم يحسبها الكود بسبب خطأ إملائي بسيط؟
    2. اكتب تحليلاً طبياً قصيراً بالعربية عن "الطلاقة اللفظية" للمريض.
    3. إذا كان العدد قريباً من 11 (مثل 10)، كن رحيماً في التحليل.
    
    رد بـ:
    Score: [{logic_res['score']}]
    Analysis: [التحليل هنا]
    """
    try:
        response = client.chat.completions.create(
            model="Qwen/Qwen2.5-7B-Instruct",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )
        return response.choices[0].message.content
    except:
        return f"Analysis: تم رصد {logic_res['count']} كلمة تبدأ بحرف الفاء."