FROM ubuntu:20.04
RUN apt update -y && apt upgrade -y && apt install python3 -y
RUN apt install python3-pip -y
RUN pip install requests
COPY main.py .
CMD python3 main.py
