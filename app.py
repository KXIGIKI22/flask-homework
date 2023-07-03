import logging

from flask import Flask

app = Flask(__name__)

@app.route('/hello')
@app.route('/html')
def html():
    app.logger.info('HTML endpoint called.')
    return '<h1>This is an HTML response</h1>'

@app.route('/json')
def json():
    app.logger.info('JSON endpoint called.')
    return {'message': 'This is a JSON response'}
def hello():
    app.logger.info('Hello endpoint called.')
    return 'Hello, world!'

if __name__ == '__main__':
    app.run()