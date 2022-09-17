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
        print(denominator)
        accurate_answers = 0

        for i in range(1, max_rating + 1):
            lower_bound = 1
            for question in interview["questions"]:

                # Stig replies
                is_valid = i >= question["lower"] and i <= question["upper"]

                if is_valid:
                    lower_bound = max(lower_bound, question["lower"])

                # if prudent_value == -1:
                #     prudent_value = 1
                # else:

                # next_possible_prudent_value = question["lower"]
                # if is_valid:
                #     prudent_value = max(next_possible_prudent_value, prudent_value)

            if lower_bound == i:
                accurate_answers += 1

        gcd = Fraction(accurate_answers, denominator)
        output.append({"p": gcd.numerator, "q": gcd.denominator})

    return jsonify(output)
