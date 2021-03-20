from flask import Flask
app = Flask(__name__)


@app.route("/roll")
def webhook_endpoint():
    return "Not implemented!"


if __name__ == '__main__':
    app.run()
