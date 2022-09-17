from fractions import Fraction

from flask import jsonify, request
from utils.firestore import Firestore

from routes import app


@app.route("/stig/warmup", methods=["POST"])
def stigwarmup():
    interview_data = request.get_json()

    output = []
    for interview in interview_data:
        max_rating = interview["maxRating"]
        denominator = max_rating
        accurate_answers = 0

        for i in range(1, max_rating + 1):
            possibleSet = set(range(1, max_rating + 1))
            for question in interview["questions"]:
                is_valid = i >= question["lower"] and i <= question["upper"]
                value_range = range(question["lower"], question["upper"] + 1)

                if is_valid:
                    possibleSet = set([x for x in possibleSet if x in value_range])
                else:
                    possibleSet = set([x for x in possibleSet if x not in value_range])

            if min(possibleSet) == i:
                accurate_answers += 1

        gcd = Fraction(accurate_answers, denominator)
        output.append({"p": gcd.numerator, "q": gcd.denominator})

    return jsonify(output)


@app.route("/stig/full", methods=["POST"])
async def stigfull():
    interview_data = request.get_json()

    db = Firestore()
    await db.create_swizz_data(interview_data)


def convert_value(original, p, lucky_number, max_rating):
    return (original + p * lucky_number - 1) % max_rating + 1
