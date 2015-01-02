from flask import Flask

#Configure the Flask server
app = Flask(__name__)
app.config.from_object('webapp.config.Config')

def import_views():
    import webapp.views
    import webapp.motorapi