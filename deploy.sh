#!/bin/bash
SITE_PATH=/var/www/catalogapp
sudo rm -rf SITE_PATH
sudo cp catalogapp.conf /etc/apache2/sites-available/catalogapp.conf
sudo cp -r catalogapp/ /var/www/
echo ${SUDO_USER}
sudo chown -R ${SUDO_USER}:${SUDO_USER} ${SITE_PATH}
mkdir -p ${SITE_PATH}/logs