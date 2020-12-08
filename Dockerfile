FROM python:3.8-slim-buster

ADD HoeWarmIsHetInDelft.py /

CMD [ "python", "./HoeWarmIsHetInDelft.py" ]