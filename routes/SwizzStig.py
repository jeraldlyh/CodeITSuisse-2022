from fractions import Fraction

from flask import jsonify, request

from routes import app


def stig_process_gcd(interview_data, pq_data=None, lucky_number=None):
    max_rating = interview_data["maxRating"]
    denominator = max_rating
    accurate_answers = 0

    for i in range(1, max_rating + 1):
        possibleSet = set(range(1, max_rating + 1))
        for question in interview_data["questions"]:
            lower_bound = question["lower"]
            higher_bound = question["upper"]

            if pq_data is not None:
                lower_bound = convert_value(
                    lower_bound, pq_data["p"], lucky_number, max_rating
                )
                higher_bound = convert_value(
                    higher_bound, pq_data["p"], lucky_number, max_rating
                )

                if lower_bound > higher_bound or higher_bound < lower_bound:
                    temp_bound = lower_bound
                    lower_bound = higher_bound
                    higher_bound = temp_bound

            is_valid = i >= lower_bound and i <= higher_bound
            value_range = range(lower_bound, higher_bound + 1)

            if is_valid:
                possibleSet = set([x for x in possibleSet if x in value_range])
            else:
                possibleSet = set([x for x in possibleSet if x not in value_range])

        if min(possibleSet) == i:
            accurate_answers += 1

    gcd = Fraction(accurate_answers, denominator)
    return {"p": gcd.numerator, "q": gcd.denominator}


@app.route("/stig/warmup", methods=["POST"])
def stigwarmup():
    interview_data = request.get_json()

    output = []
    for interview in interview_data:
        output.append(stig_process_gcd(interview))

    return jsonify(output)


@app.route("/stig/full", methods=["POST"])
async def stigfull():
    interview_data = request.get_json()
    interviews = {}  # {index: pq_data}

    for index, interview in enumerate(interview_data):
        if index - 1 not in interviews:
            interviews[index] = stig_process_gcd(interview)
        else:
            interviews[index] = stig_process_gcd(
                interview, interviews[index - 1], interview["lucky"]
            )
    print(interviews)
    return jsonify([v for k, v in interviews.items()])


def convert_value(original, p, lucky_number, max_rating):
    return (original + p * lucky_number - 1) % max_rating + 1
