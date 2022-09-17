import logging

from dotenv import load_dotenv

from routes import app

load_dotenv()


@app.route("/")
def hello():
    return "Hello, World!"


logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

logging.info("Server has started")
