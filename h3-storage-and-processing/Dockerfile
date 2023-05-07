FROM python

WORKDIR /source

COPY requirements.txt .
COPY requirements-dev.txt .

RUN pip install -r requirements.txt -r requirements-dev.txt

COPY client client
COPY tests tests

ENTRYPOINT [ "python", "-m", "pytest" ]