from webapp import app, import_views
from webapp.config import MalinaConfig
from os import environ


if __name__ == '__main__':
    app.config.from_object(MalinaConfig)
    import_views()
    #HOST = environ.get('SERVER_HOST', 'localhost')
    #try:
    #    PORT = int(environ.get('SERVER_PORT', '5555'))
    #except ValueError:
    #    PORT = 5555
    PORT = 5555
    app.run(host='0.0.0.0', port=PORT)