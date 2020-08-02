# FROM ubuntu:16.04
FROM ubuntu:latest
LABEL TuanNa "nguyentuan4989@gmail.com"
WORKDIR /ocrdemo

RUN apt-get update && DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata
RUN apt-get install -y python3-pip python3-dev python3-venv \
    && apt-get install -y curl tesseract-ocr libtesseract-dev libleptonica-dev pkg-config vim \
    && cd /usr/local/bin \
    && ln -s /usr/bin/python3 python
RUN pip3 install --upgrade pip \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3

# Set up and activate virtual environment
ENV VIRTUAL_ENV "/venv"
RUN python -m venv $VIRTUAL_ENV
ENV PATH "$VIRTUAL_ENV/bin:$PATH:/root/.poetry/bin"

COPY ./pyproject.toml /ocrdemo

# Error: /bin/sh: poetry: not found.
# Sol: To get started you need Poetry's bin directory ($HOME/.poetry/bin) in your `PATH` environment variable.
# ENV PATH="${PATH}:/root/.poetry/bin"
RUN poetry update \
    # && poetry add tesserocr \
    && poetry install

ENTRYPOINT ["python3"]
# ENTRYPOINT ["python3"]
# CMD ["-o", "/ocrdemo/output.txt"]