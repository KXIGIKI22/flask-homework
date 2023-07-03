import logging
from flask import Flask

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

@app.route('/hello')
def hello():
    app.logger.info('Hello endpoint called')
    return 'Hello, world!'

@app.route('/html')
def return_html():
    app.logger.info('HTML endpoint called')
    return '<h1>This is an HTML response</h1>'

@app.route('/json')
def return_json():
    app.logger.info('JSON endpoint called')
    return {'message': 'This is a JSON response'}

if __name__ == '__main__':
    app.run()