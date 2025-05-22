FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p result data

ENV QT_X11_NO_MITSHM=1
ENV QT_QUICK_BACKEND="software"
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /root/.config/Ultralytics && \
    chmod -R 777 /root/.config

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"] 