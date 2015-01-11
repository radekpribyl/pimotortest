import atexit
from webapp import app, import_views, socketio
from webapp.config import MalinaConfig
from os import environ

#Enable remote debugging
import ptvsd
ptvsd.enable_attach(secret = 'malina')

@atexit.register
def robot_cleanup_on_exit():
    print("Robot cleanup")
    app.config["ROBOT"].cleanup()


if __name__ == '__main__':
    app.config.from_object(MalinaConfig)
    import_views()
    #HOST = environ.get('SERVER_HOST', 'localhost')
    #try:
    #    PORT = int(environ.get('SERVER_PORT', '5555'))
    #except ValueError:
    #    PORT = 5555
    #PORT = 5555
    #app.run(host='0.0.0.0', port=PORT)

    socketio.run(app, host='0.0.0.0')