from fractions import Fraction

from flask import jsonify, request
from utils.firestore import Firestore

from routes import app


@app.route("/stig/warmup", methods=["POST"])
async def stigwarmup():
    interview_data = request.get_json()

    db = Firestore()
    await db.create_swizz_data(interview_data)

    output = []
    for interview in interview_data:
        max_rating = interview["maxRating"]
        denominator = max_rating * len(interview["questions"])
        accurate_answers = 0

        prudent_value = 1

        for i in range(1, max_rating + 1):
            for question in interview["questions"]:
                next_possible_prudent_value = question["lower"]

                # Stig replies
                is_valid = i >= question["lower"] and i <= question["upper"]

                if is_valid:
                    prudent_value = max(next_possible_prudent_value, prudent_value)

                if prudent_value == i:
                    accurate_answers += 1

        gcd = Fraction(accurate_answers, denominator)
        output.append({"p": gcd.numerator, "q": gcd.denominator})

    return jsonify(output)
