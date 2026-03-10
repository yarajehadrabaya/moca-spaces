from huggingface_hub import InferenceClient
import os

client = InferenceClient(api_key=os.getenv("HF_TOKEN"))

def analyze_attention(q_type, text, score, max_s):
    prompt = f"""
    أنت طبيب أعصاب خبير. قم بالتعليق على أداء مريض في اختبار {q_type}.
    كلام المريض: "{text}"
    الدرجة التي حصل عليها (برمجياً): {score} من {max_score if 'max_score' in locals() else max_s}.
    
    المطلوب:
    - اكتب تقريراً طبياً مختصراً بالعربية.
    - إذا كان السكور {max_s}، أثنِ على تركيز المريض.
    - إذا كان السكور أقل، وضح أن هناك تشتت بسيط.
    - لا تنتقد نطق الأرقام أو العامية (مثل اتنين وتلاتة)، اعتبرها صحيحة طالما الترتيب سليم.
    """
    try:
        res = client.chat.completions.create(
            model="Qwen/Qwen2.5-7B-Instruct",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=350
        )
        return res.choices[0].message.content
    except:
        return f"التحليل الطبي: حصل المريض على {score} من {max_s}."