from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    print("Execute command!")
    return 'Hello World!'

@app.route('/second_command/')
def not_hello_world():
    print("Execute second command!")
    return 'Goodbye World!'

if __name__ == '__main__':
    app.run()
