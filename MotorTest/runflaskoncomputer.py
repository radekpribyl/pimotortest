from __future__ import print_function
import atexit
from webapp import app, import_views, socketio
from webapp.config import TestingConfig

@atexit.register
def robot_cleanup_on_exit():
    print("Robot cleanup")
    app.config["ROBOT"].cleanup()

if __name__ == '__main__':
    app.config.from_object(TestingConfig)
    import_views()
    
    socketio.run(app, host='0.0.0.0')
