FROM resin/rpi-raspbian:jessie:jessie-20180109

RUN apt-get update && apt-get install -y wget

RUN wget -q -O - http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key | apt-key add -
RUN wget -q -O /etc/apt/sources.list.d/mosquitto-jessie.list http://repo.mosquitto.org/debian/mosquitto-jessie.list
RUN apt-get update && apt-get install -y mosquitto

RUN adduser --system --disabled-password --disabled-login mosquitto
COPY ./mosquitto.conf /etc/mosquitto/mosquitto.conf
RUN echo "" > /etc/mosquitto/pwfile
RUN mosquitto_passwd -b /etc/mosquitto/pwfile user your_password

EXPOSE 1883

CMD /usr/sbin/mosquitto -c /etc/mosquitto/mosquitto.conf