# Udacity Item Catalog 
_______________________
## About
This is a Item Catalog app. It provides a list of items within a variety of categories.
You can login the app using Google login. Logined users will have the ability to post, edit and delete their own items. This project is implemented using Python3 Flask and Sqlite.

## Deploy the Project
This project can be deployed to a Ubuntu server using the following step.
As an example, the project is deployed to an Amazon Lightsail server.
You can access the website from http://http://34.209.212.196.xip.io

### Prerequisites
* [Python 3](https://www.python.org/downloads/)
* Apache2
  ```
  sudo apt-get install apache2
  ```
* libapache2-mod-wsgi-py3
  ```
  sudo apt-get install libapache2-mod-wsgi-py3
  ```
* python3-venv
  ```
  sudo apt-get install python3-venv
  ```

### Setup the python virtual evnironment
Setup the project's python environment by running the following commend in
the repo directory.
```
cd catalogapp
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt 
python3 init_categories.py
```

### Depoly the app to apache2
Edit the catalogapp.conf file and make sure the user and group name matches the one you use on your server. Then run the deploy.sh script to deploy the app.
```
sudo sh deploy.sh
```

### For Udacity Grader
You can ssh the server using the username **grader** at 34.209.212.196 with port number 2200. A public key has already been setup for your access.
