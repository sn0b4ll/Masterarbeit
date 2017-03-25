FROM ubuntu:16.10
RUN apt-get update

# Set bash
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# Supervisor
RUN DEBIAN_FRONTEND=noninteractive apt-get -yq install supervisor
run mkdir -p /var/log/supervisor

RUN apt-get update && apt-get upgrade -y

## Python 3.6
RUN apt-get install -y \
  python3.6 \
  python3.6-dev \
  python3-pip \
  supervisor \
  && apt-get autoremove \
  && apt-get clean

RUN python3.6 -m pip install pip --upgrade

# Folders
run mkdir -p /var/log/supervisor

RUN mkdir -p /opt/pentest-helper
RUN mkdir -p /opt/pentest-helper/compile/report/bilder
RUN mkdir -p /opt/pentest-helper/compile/report/configs
RUN mkdir -p /opt/pentest-helper/compile/report/screenshots
RUN mkdir -p /opt/pentest-helper/download
RUN mkdir -p /opt/pentest-helper/static
RUN mkdir -p /opt/pentest-helper/templates/fragebogen
RUN mkdir -p /opt/pentest-helper/templates/report
RUN mkdir -p /opt/pentest-helper/templates_tex/report
RUN mkdir -p /opt/pentest-helper/tex/download
RUN mkdir -p /opt/pentest-helper/tex/report
RUN mkdir -p /opt/pentest-helper/uploads

# Requirements
COPY requirements.txt /opt/pentest-helper/requirements.txt
RUN python3.6 -m pip install -r /opt/pentest-helper/requirements.txt

# Copy Code-Files
COPY compile/report/bilder/* /opt/pentest-helper/compile/report/bilder/
COPY compile/report/configs/* /opt/pentest-helper/compile/report/configs/
COPY static/* /opt/pentest-helper/static/
COPY templates/fragebogen/* /opt/pentest-helper/templates/fragebogen/
COPY templates/report/* /opt/pentest-helper/templates/report/
COPY templates/* /opt/pentest-helper/templates/
COPY templates_tex/report/* /opt/pentest-helper/templates_tex/report/
COPY templates_tex/* /opt/pentest-helper/templates_tex/
COPY tex/* /opt/pentest-helper/tex/
COPY clean.sh /opt/pentest-helper/clean.sh
COPY pentest_helper.py /opt/pentest-helper/pentest_helper.py
COPY pentest_templates.py /opt/pentest-helper/pentest_templates.py
COPY run_docker.py /opt/pentest-helper/run.py

#CMD ["/usr/bin/python3.6", "/opt/pentest-helper/run.py"]

# Supervisor
# COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
# CMD ["/usr/bin/supervisord"]

EXPOSE 5000
