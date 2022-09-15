from dotenv import load_dotenv

from routes import app

load_dotenv()


@app.route("/")
def hello():
    return "Hello, World!"
