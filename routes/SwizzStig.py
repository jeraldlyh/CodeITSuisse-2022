import logging
from fractions import Fraction

from flask import jsonify, request

from routes import app


@app.route("/stig/warmup", methods=["POST"])
def stigwarmup():
    input_data = request.get_json()

    output = []
    for input in input_data:
        max_rating = input["maxRating"]
        denominator = max_rating * len(input["questions"])
        accurate_answers = 0

        for j in range(len(input["questions"])):
            prudent_value = 1

            logging.info(accurate_answers, denominator)
            for i in range(1, max_rating + 1):
                for question in input["questions"]:
                    value_pass = question["lower"]

                    # Stig replies
                    is_valid = i >= question["lower"] and i <= question["upper"]

                    if is_valid:
                        prudent_value = max(value_pass, prudent_value)

                if prudent_value == i:
                    accurate_answers += 1

        gcd = Fraction(accurate_answers, denominator)
        output.append({"p": gcd.numerator, "q": gcd.denominator})

    return jsonify(output)
