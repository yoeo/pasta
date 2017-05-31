FROM python:3

RUN mkdir /app
WORKDIR /app
ADD . /app/

RUN pip3 install .

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "-w", "4", "pasta:app"]
