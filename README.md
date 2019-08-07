# Udacity Item Catalog 
_______________________
## About
This is a Item Catalog app. It provides a list of items within a variety of categories.
You can login the app using Google login. Logined users will have the ability to post, edit and delete their own items.

## Prerequisites
* [Python 3](https://www.python.org/downloads/)
* [VirtualBox 3](https://www.virtualbox.org/) - The VM software.
* [Vagrant](https://www.vagrantup.com/) - The software that configures the VM.

## Project Setup
Follow these step to setup and run this project:
### Download and unzip the VM configuration file:
  [FSND-Virtual-Machine.zip](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip).
  This will give you a directory called FSND-Virtual-Machine, which containing the VM files. Change
  to this directory in your terminal with cd. Inside, you will find another
  directory called vagrant. Change directory to the vagrant directory. Then copy the entire project 
  directory to the vagrant directory.
### Start the virtual machine
  From your terminal, inside the vagrant subdirectory, run the command: 
  ```
  vagrant up
  ```
  This will cause Vagrant to download the Linux operating system and install it.
  This may take quite a while (many minutes) depending on how fast your Internet
  connection is. When vagrant up is finished running, you will get your shell
  prompt back. At this point, you can run 
  ```
  vagrant ssh
  ```
  to log in to your newly installed Linux VM.
### Install additional dependencies
  This project requires some additional dependencies except those included in the virtual machine.
  You can install those dependencies after ssh to the virtual machine using pip:
    ```
     pip3 install flask_sqlalchemy --user
     pip3 install google-oauth --user
    ```
### Setup the database
    Initialize the database by running the init_categories.py script.
    ```
    python3 init_categories.py
    ```
### Running the server
    Run the server on the virtual machine.
    ```
    python3 application.py
    ```
    Now you should be able to access the app on your own machin using http://localhost:8000

### Login to add your own items
    Without login, you can browse other items added by other users. Once you login, you can 
    add, edit and delete your own item. You can login using your Google account.