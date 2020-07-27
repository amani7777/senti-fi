FROM python:3.8

EXPOSE 8080


WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD streamlit run --server.port 8080 --server.enableCORS false app.py