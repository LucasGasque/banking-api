FROM python:3.12

ENV ROOT=/code

COPY app $ROOT/app

COPY requirements/run.txt $ROOT/requirements.txt

WORKDIR $ROOT

RUN python3.12 -m pip install --upgrade pip

RUN python3.12 -m pip install --no-cache-dir -r requirements.txt

CMD ["python3.12", "-m", "app"]