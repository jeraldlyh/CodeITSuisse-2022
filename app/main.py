import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from stats import to_cumulative, to_cumulative_delayed

load_dotenv()

print(os.environ.get('FLASK_APP'))

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route("/tickerStreamPart1", methods=["POST"])
def ticker_stream_part_one():
    print(request.get_json())
    input_data = request.get_json()["stream"]
    
    return jsonify({"output": to_cumulative(input_data)})

@app.route("/tickerStreamPart2", methods=["POST"])
def ticker_stream_part_two():
    input_data = request.get_json()["stream"]
    quantity_block = request.get_json()["quantityBlock"]
    
    return jsonify({"output": to_cumulative_delayed(input_data, quantity_block)})
