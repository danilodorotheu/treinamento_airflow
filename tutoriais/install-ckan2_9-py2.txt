#!/bin/bash

sudo apt update
sudo apt install -y libpq5 redis-server nginx supervisor postgresql solr-tomcat

# INSTALL CKAN
sudo apt install -y libpython2.7
wget http://packaging.ckan.org/python-ckan_2.9-py2-focal_amd64.deb
sudo dpkg -i python-ckan_2.9-py2-focal_amd64.deb

# CREATE USER POSTGRES ckan_default
sudo -u postgres psql -l
sudo -u postgres createuser -S -D -R ckan_default
sudo -u postgres psql -c "ALTER ROLE ckan_default WITH PASSWORD 'teste123';"
sudo -u postgres createdb -O ckan_default ckan_default -E utf-8

# TOMCAT CONFIGURATION
sudo sed -i -e "s;Connector port=\"8080\" protocol=\"HTTP/1.1\";Connector port=\"8983\" protocol=\"HTTP/1.1\";g" /etc/tomcat9/server.xml

# SOLR CONFIGURATION
sudo mv /etc/solr/conf/schema.xml /etc/solr/conf/schema.xml.bak
sudo ln -s /usr/lib/ckan/default/src/ckan/ckan/config/solr/schema.xml /etc/solr/conf/schema.xml
sudo sed -i -e "s;\#solr_url = http://127.0.0.1:8983/solr;solr_url = http://127.0.0.1:8983/solr;g" /etc/ckan/default/ckan.ini

sudo service tomcat9 restart

# IP CONFIGURATION
PUBLIC_IP=$(dig +short myip.opendns.com @resolver1.opendns.com)
echo $PUBLIC_IP
sudo sed -i -e "s;ckan.site_url =;ckan.site_url = http://$PUBLIC_IP;g" /etc/ckan/default/ckan.ini

# DATABASE CONFIGURATION
sudo sed -i -e "s;postgresql://ckan_default:pass@localhost/ckan_default;postgresql://ckan_default:teste123@localhost/ckan_default;g" /etc/ckan/default/ckan.ini
sudo ckan db init

sudo service nginx restart

# APPLY DATASTORE
sudo mkdir -p /var/lib/ckan/default
ckan.storage_path = /var/lib/ckan/default
sudo chown www-data:www-data /var/lib/ckan/default
sudo chmod u+rwx /var/lib/ckan/default

sudo sed -i -e "s;\#ckan.storage_path = /var/lib/ckan;ckan.storage_path = /var/lib/ckan/default;g" /etc/ckan/default/ckan.ini
sudo sed -i -e "s;ckan.plugins = stats text_view image_view recline_view;ckan.plugins = stats text_view image_view recline_view datastore;g" /etc/ckan/default/ckan.ini

sudo sed -i -e "s;\#ckan.datastore.write_url = postgresql://ckan_default:pass@localhost/datastore_default;ckan.datastore.write_url = postgresql://ckan_default:teste123@localhost/datastore_default;g" /etc/ckan/default/ckan.ini
sudo sed -i -e "s;\#ckan.datastore.read_url = postgresql://datastore_default:pass@localhost/datastore_default;ckan.datastore.read_url = postgresql://datastore_default:teste123@localhost/datastore_default;g" /etc/ckan/default/ckan.ini

sudo -u postgres createuser -S -D -R -l datastore_default
sudo -u postgres psql -c "ALTER ROLE datastore_default WITH PASSWORD 'teste123';"
sudo -u postgres createdb -O ckan_default datastore_default -E utf-8

sudo ckan -c /etc/ckan/default/ckan.ini datastore set-permissions | sudo -u postgres psql --set ON_ERROR_STOP=1

sudo supervisorctl reload

echo "FINALIZADO"
