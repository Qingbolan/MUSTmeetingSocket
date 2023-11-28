from flask import Flask
from app import create_app, socketio



if __name__ == '__main__':
    app = Flask(__name__, static_folder='static', static_url_path='/static', template_folder='templates')
    app = create_app(app)
    socketio.run(app, debug=True, host='0.0.0.0', port=7100)
