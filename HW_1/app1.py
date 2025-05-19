from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Flask!'

@app.route('/name/<name>')
def hello_name(name):
    return f'Hello, {name}!'


if __name__ == '__main__':
    app.run(port=5001,debug=True)