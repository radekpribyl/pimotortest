from flask import Flask
from flask_socketio import SocketIO

#Configure the Flask server
app = Flask(__name__)
#app.config.from_object('webapp.config.Config')
socketio = SocketIO(app)

def import_views():
    import webapp.views
    import webapp.motorapi
