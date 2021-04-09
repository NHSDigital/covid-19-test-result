from flask import Flask
app = Flask(__name__)


@app.route('/', defaults={"path": ""})
@app.route('/<path:path>')
def hello_world(path):
    return f"Hello world test! Path: {path}"
