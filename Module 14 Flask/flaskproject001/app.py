from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/home')
def hello_home():
    return render_template('sample.html')




if __name__ == '__main__':
    app.run(debug=True)