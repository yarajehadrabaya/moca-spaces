from huggingface_hub import InferenceClient
import os
from datetime import datetime

HF_TOKEN = os.getenv("HF_TOKEN")
client = InferenceClient(api_key=HF_TOKEN)

def analyze_orientation(patient_text_summary, real_place, real_city):
    now = datetime.now()
    
    months_map = {
        1: ["يناير", "كانون الثاني", "واحد", "1"],
        2: ["فبراير", "شباط", "اتنين", "تنين", "اثنين", "2"],
        3: ["مارس", "آذار", "ثلاثة", "تلاتة", "3"],
        4: ["أبريل", "نيسان", "اربعة", "4"],
        5: ["مايو", "أيار", "خمسة", "5"],
        6: ["يونيو", "حزيران", "ستة", "6"],
        7: ["يوليو", "تموز", "سبعة", "7"],
        8: ["أغسطس", "آب", "ثمانية", "تمانية", "8"],
        9: ["سبتمبر", "أيلول", "تسعة", "9"],
        10: ["أكتوبر", "تشرين الأول", "عشرة", "10"],
        11: ["نوفمبر", "تشرين الثاني", "أحد عشر", "دعش", "11"],
        12: ["ديسمبر", "كانون الأول", "اثنا عشر", "طنعش", "12"]
    }

    arabic_days = {
        "Monday": "الاثنين", "Tuesday": "الثلاثاء", "Wednesday": "الأربعاء",
        "Thursday": "الخميس", "Friday": "الجمعة", "Saturday": "السبت", "Sunday": "الأحد"
    }
    
    current_day_name = arabic_days.get(now.strftime("%A"), now.strftime("%A"))
    current_month_num = now.month
    current_month_options = months_map[current_month_num]

    prompt = f"""
    أنت طبيب أعصاب خبير . قيم إجابات مريض في اختبار التوجه (Orientation).
    
    الحقائق الحقيقية الآن:
    1. يوم الأسبوع: {current_day_name}
    2. الشهر الحالي: هو الشهر رقم ({current_month_num}) واسمه ({current_month_options[0]}).
    3. السنة الحالية: {now.strftime('%Y')}
    4. المكان المتوقع: {real_place}
    5. المدينة المتوقعة: {real_city}

    إجابات المريض المستخرجة من التسجيلات:
    {patient_text_summary}

    المطلوب منك (قواعد التصحيح المرنة جداً):
    - بالنسبة لـ "الشهر": إذا قال المريض رقم الشهر (مثلاً "واحد" أو "1") أو اسمه (يناير)، اعتبرها صحيحة 100%.
    - اقبل اللهجات العامية تماماً (مثل: "طنعش" لشهر 12، "تنين" لشهر 2، "خمسة وعشرين" لسنة 2025).
    - بالنسبة لـ "المكان": إذا قال (بيتنا، دارنا، حارتنا) وكان المكان المتوقع هو منزله، فهي صحيحة.
    - احسب السكور النهائي من 5 (نقطة لكل إجابة صحيحة).

    رد بالتنسيق التالي حصراً:
    Score: [الرقم من 0-5]
    Analysis: [شرح طبي مختصر بالعربي لكل نقطة]
    """

    try:
        response = client.chat.completions.create(
            model="Qwen/Qwen2.5-7B-Instruct",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Score: 0\nAnalysis: خطأ فني في الاتصال بالموديل: {str(e)}"
