#!/usr/bin/python3
import sys
sys.path.insert(0,"/var/www/FLASKAPPS/")
sys.stdout = sys.stderr
print(sys.version)
from catalogapp.application import app as application
application.secret_key = "super_secret_key"
