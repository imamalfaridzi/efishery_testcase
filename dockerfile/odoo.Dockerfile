FROM odoo:14.0
USER root

RUN apt update

RUN apt-get install apt-utils python3-dev -y

RUN python3 -m pip install setuptools wheel

RUN python3 -m pip install pyjwt