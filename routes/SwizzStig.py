from fractions import Fraction

from flask import jsonify, request

from routes import app


@app.route("/stig/warmup", methods=["POST"])
async def stigwarmup():
    interview_data = request.get_json()

    # db = Firestore()
    # await db.create_swizz_data(interview_data)

    output = []
    for interview in interview_data:
        max_rating = interview["maxRating"]
        denominator = max_rating
        accurate_answers = 0

        for i in range(1, max_rating + 1):
            possibleSet = set(range(1, max_rating + 1))
            for question in interview["questions"]:
                is_valid = i >= question["lower"] and i <= question["upper"]
                valueRange = range(question["lower"], question["upper"] + 1)
                if not is_valid:
                    possibleSet = set([x for x in possibleSet if x not in valueRange])

                if is_valid:
                    possibleSet = set([x for x in possibleSet if x in valueRange])

            if min(possibleSet) == i:
                accurate_answers += 1

        gcd = Fraction(accurate_answers, denominator)
        output.append({"p": gcd.numerator, "q": gcd.denominator})

    return jsonify(output)
