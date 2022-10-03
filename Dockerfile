FROM python:3.10-bullseye

RUN mkdir -p /opt/app

COPY . /opt/app

WORKDIR /opt/app

RUN python -m venv /opt/app/venv

ENV PATH=/opt/app/venv/bin:$PATH

RUN apt update 

RUN apt install git --no-install-suggests --no-install-recommends -y

RUN python -m pip install --upgrade pip

RUN pip install wheel setuptools

RUN pip install -r requirements.txt -v

CMD [ "python", "-m", "bot" ]
