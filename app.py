from flask import Flask
from time import  sleep

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


def runworker():
    pass


def runserver():
    app.run(host="0.0.0.0", debug=True)


if __name__ == '__main__':
    runworker()
    runserver()
