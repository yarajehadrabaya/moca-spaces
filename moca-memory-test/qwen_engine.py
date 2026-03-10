from huggingface_hub import InferenceClient
import os

HF_TOKEN = os.getenv("HF_TOKEN")
client = InferenceClient(api_key=HF_TOKEN)

def get_memory_analysis(logic_results):
    prompt = f"""
    أنت طبيب أعصاب خبير ورحيم جداً. قم بتقييم استرجاع الكلمات لمريض مسن.
    الكلمات المطلوبة: (راس، مخمل، برج، ورد، بني).
    
    ما سمعه النظام من المريض: "{logic_results['original_text']}"
    الكلمات التي اكتشفها الكود برمجياً: {logic_results['matched_words']}
    
    المطلوب منك:
    1. راجع النص المسموع بعناية. هل هناك كلمات صحيحة أخطأ المحول الصوتي في كتابتها؟
       (مثلاً: 'وارد' هي 'ورد'، 'رقص' هي 'راس'، 'مخمر' هي 'مخمل').
    2. إذا وجدتها، احتسبها صحيحة وارفع الدرجة.
    3. كن مرناً جداً مع لهجات كبار السن.

    يجب أن يكون ردك بهذا التنسيق حصراً لضمان الدقة:
    Score: [الرقم النهائي من 0 إلى 5]
    Analysis: [تحليل طبي مشجع بالعربية]
    """
    try:
        response = client.chat.completions.create(
            model="Qwen/Qwen2.5-7B-Instruct",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Score: {logic_results['matched_count']}\nAnalysis: خطأ في الاتصال. تم احتساب الدرجة آلياً."