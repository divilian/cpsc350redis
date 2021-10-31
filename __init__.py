
from flask import Flask
hobby_mgr = Flask(__name__)
from cpsc350redis import routes

hobby_mgr.secret_key = "Tunafish forever!"
