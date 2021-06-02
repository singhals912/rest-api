FROM tensorflow/tensorflow

COPY requirements.txt . 

RUN pip install -r requirements.txt 

COPY Assignment2.py /app/Assignment2.py
COPY answer_test.py /app/answer_test.py

CMD ["python3", "/app/Assignment2.py"]
