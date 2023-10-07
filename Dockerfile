FROM python:3.11

WORKDIR /app

ADD . .

RUN pip install -r requirements.txt

CMD ["streamlit", "run", "💬_Chat_with_AI.py"]