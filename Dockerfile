FROM ubuntu:20.04
WORKDIR /home/app

COPY requirements.txt .
RUN apt-get update
RUN apt-get install -y python3.8
RUN apt-get install -y python3-venv
RUN apt-get install -y python3-pip
RUN python3 -m venv .venv
RUN pip3 install -r requirements.txt


COPY flashcard flashcard
COPY main.py config.py boot.sh ./
RUN chmod 700 boot.sh

# run-time configuration
EXPOSE 5555
ENTRYPOINT ["./boot.sh"]