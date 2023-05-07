FROM python:3.11-alpine

WORKDIR /home

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV PATH=/root/.local/bin:$PATH

CMD ["python", "app/app.py"]
