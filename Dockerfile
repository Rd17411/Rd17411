FROM python:3.10

RUN apt-get update && apt-get install -y apt-utils build-essential python3-dev wget wkhtmltopdf python3-pip

RUN pip3.10 install virtualenv

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

RUN echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google.list

RUN apt-get update && apt-get install -y google-chrome-stable

COPY . /ddc-regression

RUN rm /ddc-regression/Dockerfile

RUN chmod -R 775 /ddc-regression/regression_sript.sh

ENTRYPOINT sh /ddc-regression/regression_sript.sh && /bin/bash
