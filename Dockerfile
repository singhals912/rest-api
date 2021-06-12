FROM tensorflow/tensorflow

COPY requirements.txt . 

RUN pip install -r requirements.txt 

COPY Assignment2.py /app/Assignment2.py
COPY test_restapi.py /app/test_restapi.py

CMD ["python3", "/app/Assignment2.py"]
