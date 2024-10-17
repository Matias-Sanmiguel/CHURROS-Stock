FROM python:3.9

WORKDIR /app

ADD main.py .

RUN pip install pandas

RUN pip install numpy

COPY archivos.json /app/
COPY credenciales.json /app/

CMD ["python","./main.py"]
