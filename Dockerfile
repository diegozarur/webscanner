FROM python:3.9-alpine

WORKDIR /code

COPY . /code

# update pip
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "--config", "gunicorn-cfg.py", "run:app"]