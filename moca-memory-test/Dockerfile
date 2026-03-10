FROM python:3.9

# تثبيت برنامج FFmpeg الضروري لتحويل صيغ الصوت
RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

# تشغيل التطبيق على البورت المخصص لـ Hugging Face
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]