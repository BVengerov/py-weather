FROM ubuntu:20.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

COPY . /
WORKDIR /
RUN pip3 install -r requirements.txt

ENV PYTHONPATH /
ENTRYPOINT [ "python3" ]
CMD [ "app/main.py" ]