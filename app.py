from flask import Flask, render_template



app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('base.html')


def runworker():
    pass


def runserver():
    app.run(host="0.0.0.0", debug=True)


if __name__ == '__main__':
    runworker()
    runserver()
