FROM python:3.10-bullseye

COPY . /opt

WORKDIR /opt

RUN python -m venv /app/venv

ENV PATH=/opt/venv/bin:$PATH

RUN apt update 

RUN apt install git --no-install-suggests --no-install-recommends -y

RUN python -m pip install --upgrade pip

RUN pip install wheel setuptools

RUN pip install -r requirements.txt -v

CMD [ "python", "-m", "bot" ]