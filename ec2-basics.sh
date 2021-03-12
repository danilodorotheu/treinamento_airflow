#!/bin/bash

########################################################
##### USE THIS FILE IF YOU LAUNCHED AMAZON LINUX 2 #####
########################################################

# get admin privileges
sudo su

yum update
yum -y install gcc python3-pip python3-devel

PATH=$PATH:/usr/local/bin

python3 -m venv /root/venv
source /root/venv/bin/activate
pip install --upgrade "pip==20.2.4"

AIRFLOW_VERSION=1.10.14
PYTHON_VERSION="$(python3 --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

mkdir /root/airflow/dags
sudo wget https://raw.githubusercontent.com/danilodorotheu/treinamento_airflow/master/helloworld.py -P /root/airflow/dags
sudo wget https://raw.githubusercontent.com/danilodorotheu/treinamento_airflow/master/data_etl.ipynb -P /root/airflow/dags

# unrar install
wget https://www.rarlab.com/rar/rarlinux-x64-5.6.1.tar.gz -P /tmp
tar -zxvf /tmp/rarlinux-x64-5.6.1.tar.gz -C /tmp
cp -v /tmp/rar/rar /tmp/rar/unrar /usr/local/bin

airflow db init

airflow webserver -D
airflow scheduler -D

pip install pandas
pip install jupyter

jupyter notebook --ip='*' --NotebookApp.token='' --NotebookApp.password='' --port 80 --notebook-dir /root/airflow/dags --no-browser --allow-root