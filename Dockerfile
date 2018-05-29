FROM resin/rpi-raspbian
RUN apt-get update && apt-get install python3 python3-dev python3-pip gcc g++
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY monitoring-client /usr/local/monitoring-client/
CMD python3 /usr/local/monitoring-client/monitor.py
