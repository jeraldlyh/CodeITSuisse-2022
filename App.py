import logging
import os

import firebase_admin
from dotenv import load_dotenv

from routes import app

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./google-credentials.json"
load_dotenv()
firebase_admin.initialize_app()


@app.route("/")
async def hello():
    return "hello world"


logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

logging.info("Server has started")
