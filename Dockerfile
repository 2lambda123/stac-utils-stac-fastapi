FROM python:3.8-slim

# Any python libraries that require system libraries to be installed will likely
# need the following packages in order to build
RUN apt-get update && apt-get install -y build-essential git

RUN pip install pipenv
ENV PIPENV_NOSPIN=true
ENV PIPENV_HIDE_EMOJIS=true

ARG install_dev_dependencies=true

WORKDIR /app

COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy --ignore-pipfile ${install_dev_dependencies:+--dev}

COPY . ./

ENV APP_HOST=0.0.0.0
ENV APP_PORT=80

RUN pipenv run pip install numpy
RUN pipenv run pip install git+https://github.com/geospatial-jeff/titiler@stac-api

ENTRYPOINT ["pipenv", "run"]
CMD uvicorn stac_api.app:app --host=${APP_HOST} --port=${APP_PORT} --reload
