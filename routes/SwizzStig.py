import logging

from flask import jsonify, request

from routes import app


@app.route("/stig/warmup", methods=["POST"])
def stigwarmup():
    input_data = request.get_json()

    output = []

    for input in input_data:
        max_rating = input["maxRating"]
        passes = 0

        for question in input["questions"]:
            logging.info(question)
            for i in range(1, max_rating + 1):
                if i >= question["lower"] and i <= question["higher"]:

                    passes += 1
            output.append({"p": passes, "q": max_rating})

    return jsonify(output)
