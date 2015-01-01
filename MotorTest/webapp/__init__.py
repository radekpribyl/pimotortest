from flask import Flask

#Configure the Flask server
app = Flask(__name__)
app.config.from_object('webapp.config.Config')

import webapp.views