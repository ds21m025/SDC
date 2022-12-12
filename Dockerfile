FROM python:3.11

LABEL maintainer="wwb"
LABEL application="covid_dashboard"

# Streamlit port
EXPOSE 8501

COPY README.md requirements.txt covid_dashboard.py /app/

WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

CMD [ "streamlit", "run", "covid_dashboard.py" ]
