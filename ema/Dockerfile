FROM python:3.9.7

RUN pip install --upgrade pip

WORKDIR /src
COPY . .

# install poetry
RUN pip install poetry
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# updating certificates
COPY cert.pem /usr/local/share/ca-certificates/cert.crt
RUN cat /usr/local/share/ca-certificates/cert.crt >> /usr/local/lib/python3.9/site-packages/certifi/cacert.pem

CMD ["python", "database.py", "create_model_db"]
