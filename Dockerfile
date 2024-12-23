FROM python:3.12-slim

RUN apt-get -qqy update && apt-get install -qqy \
    curl \
    git \
    yamllint

RUN pip install --upgrade pip

WORKDIR /opt/cliapp

COPY dist/*.whl ./

RUN pip install --no-cache-dir *.whl

ENTRYPOINT ["cliapp"]
