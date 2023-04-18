FROM python:3 as base

WORKDIR /app

FROM base as ml
CMD [ "python", "-c", "import time; print('Training a model...'); time.sleep(2); print(f'f(x) = {0.42} x + {1.0}')" ]

FROM base as webapp
CMD [ "python", "-m", "http.server", "8080" ]
