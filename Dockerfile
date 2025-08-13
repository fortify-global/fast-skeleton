FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/fortify

WORKDIR /fortify

COPY requirements.txt /fortify/
RUN pip install --no-cache-dir -r /fortify/requirements.txt

COPY . /fortify

EXPOSE 8000

CMD ["uvicorn", "main:a_i", "--host", "0.0.0.0", "--port", "8000"]


