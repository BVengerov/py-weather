FROM ubuntu:20.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

ARG project_path="/py-weather"
COPY . $project_path
WORKDIR $project_path
RUN pip3 install -r requirements.txt

ENV PYTHONPATH $project_path