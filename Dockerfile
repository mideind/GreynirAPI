FROM pypy:3.7-7.3.3-slim

# Update aptitude with new repo and install software 
RUN apt-get update \
    && apt-get install -y git git-lfs build-essential

RUN apt-get install -y locales \
    && rm -rf /var/lib/apt/lists/* \
    && localedef -i is_IS -c -f UTF-8 -A /usr/share/locale/locale.alias is_IS.UTF-8

ENV LANG is_IS.utf8
ENV LANGUAGE is_IS:is

# Clone the GreynirAPI repo
RUN mkdir -p /usr/src/app
RUN cd /usr/src/app \
    && git clone https://github.com/mideind/GreynirAPI.git

# Install requirements
RUN cd /usr/src/app/GreynirAPI \
    && pip install --upgrade pip \
    && pip install --no-cache-dir git+https://github.com/mideind/GreynirPackage#egg=reynir \
    && pip install --no-cache-dir -r requirements.txt

WORKDIR /usr/src/app/GreynirAPI

EXPOSE 8080

# Run FastAPI server on port 8080
ENTRYPOINT uvicorn main:app --port 8080 --host 0.0.0.0
