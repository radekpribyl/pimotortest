from webapp import app
from webapp.config import DevelopmentConfig
from os import environ


if __name__ == '__main__':
    app.config.from_object(DevelopmentConfig)
    #HOST = environ.get('SERVER_HOST', 'localhost')
    #try:
    #    PORT = int(environ.get('SERVER_PORT', '5555'))
    #except ValueError:
    #    PORT = 5555
    PORT = 5555
    app.run(host='0.0.0.0', port=PORT)