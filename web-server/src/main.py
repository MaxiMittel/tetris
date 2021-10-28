from flask import Flask
from flask_cors import CORS

app = Flask(__name__, static_folder='../../tetris-web/build', static_url_path='/')
CORS(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

# The routing is handled by the client via React Router.
@app.errorhandler(404)   
def not_found(e):   
  return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000)