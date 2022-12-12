FROM python:3.11

LABEL maintainer="wwb"
LABEL application="covid_dashboard"

# Streamlit port
EXPOSE 80

ARG CONTAINER_VERSION
ENV CONTAINER_VERSION=${CONTAINER_VERSION}

COPY README.md requirements.txt covid_dashboard.py /app/

WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN echo $CONTAINER_VERSION >container_version.txt

CMD [ "streamlit", "run", "covid_dashboard.py", "--server.port", "80" ]
