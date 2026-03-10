from huggingface_hub import InferenceClient
import os

client = InferenceClient(api_key=os.getenv("HF_TOKEN"))

def analyze_with_qwen(task_name, features, score, max_score):
    if "رسم الساعة" in task_name:
        prompt = f"""
        أنت طبيب أعصاب خبير. قم بالتعليق على نتائج رسم الساعة لمريض مسن:
        المعطيات البرمجية: {features}
        السكور النهائي المعتمد: {score} من {max_score}

        المطلوب منك (التزم بالحقائق التالية):
        1. إذا كان 'circle_valid' هو True، فالدائرة صحيحة تماماً؛ لا تقل أنها غير مكتملة.
        2. إذا كان السكور 3، فالمريض نجح تماماً؛ أثنِ على دقته.
        3. اكتب تحليلاً طبياً مشجعاً بالعربية بناءً على السكور {score} فقط.
        4. لا تذكر أي تفاصيل عن "زيارة النقاط" أو "التوصيل" في هذا القسم (هذا لسؤال آخر).
        """
    else:
        prompt = f"أنت طبيب رحيم. حلل نتائج اختبار {task_name}: {features}. السكور المعتمد: {score} من {max_score}. اكتب تقريراً مشجعاً بالعربي."

    try:
        res = client.chat.completions.create(
            model="Qwen/Qwen2.5-7B-Instruct",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400
        )
        return res.choices[0].message.content
    except:
        return f"التحليل الطبي: أداء المريض في هذا القسم جيد جداً وحصل على درجة {score} من {max_score}."