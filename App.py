import logging
import os

import firebase_admin
from dotenv import load_dotenv

from routes import app
from utils.firestore import Firestore

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./google-credentials.json"
load_dotenv()
firebase_admin.initialize_app()


@app.route("/")
async def hello():
    db = Firestore()
    data = await db.get_swizz_data(1)
    print(data)
    return data


logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

logging.info("Server has started")
