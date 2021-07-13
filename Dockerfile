#########최신#############
FROM python:3.6

WORKDIR /usr/src/pororo_api

RUN pip install --upgrade pip
RUN python -m pip install -U pip --user

## Install packages
COPY requirement.txt ./

RUN pip install -r requirement.txt --ignore-installed

COPY . .

EXPOSE 9000

CMD ["bash", "start.sh"]
