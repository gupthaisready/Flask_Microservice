FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=app.py
ENV FLASK_DEBUG=1

COPY ./app.py ./app.py

CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0" ]

