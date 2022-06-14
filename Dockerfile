FROM python:3.9-alpine
WORKDIR /home/app

COPY requirements.txt .
RUN apk update && apk add python3-dev \
    gcc \
    libc-dev \
    libffi-dev \
    musl-dev \
    openssl-dev \
    cargo

RUN pip install -r requirements.txt

COPY flashcard flashcard
COPY main.py config.py boot.sh ./
RUN chmod 700 boot.sh

# run-time configuration
EXPOSE 5555
ENTRYPOINT ["./boot.sh"]