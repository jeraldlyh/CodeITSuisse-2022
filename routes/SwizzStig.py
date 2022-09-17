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


def stig_process_gcd_new(max_rating, questions):
    denominator = max_rating
    accurate_answers = 0

    for i in range(1, max_rating + 1):
        possibleSet = set(range(1, max_rating + 1))
        for question in questions:
            lower_bound = question["lower"]
            higher_bound = question["upper"]

            is_valid = i >= lower_bound and i <= higher_bound
            value_range = range(lower_bound, higher_bound + 1)

            if is_valid:
                possibleSet = set([x for x in possibleSet if x in value_range])
            else:
                possibleSet = set([x for x in possibleSet if x not in value_range])

        if min(possibleSet) == i:
            accurate_answers += 1

    gcd = Fraction(accurate_answers, denominator)
    return gcd.numerator, gcd.denominator


@app.route("/stig/warmup", methods=["POST"])
def stigwarmup():
    interview_data = request.get_json()

    output = []
    for interview in interview_data:
        output.append(stig_process_gcd(interview))

    return jsonify(output)


def convert_value(original, p, lucky_number, max_rating):
    return (original + p * lucky_number - 1) % max_rating + 1


def get_new_ques(lower_bound, higher_bound, p, lucky_number, max_rating):
    lower_bound = convert_value(lower_bound, p, lucky_number, max_rating)

    higher_bound = convert_value(higher_bound, p, lucky_number, max_rating)

    if lower_bound > higher_bound or higher_bound < lower_bound:
        temp_bound = lower_bound
        lower_bound = higher_bound
        higher_bound = temp_bound

    return lower_bound, higher_bound


@app.route("/stig/full", methods=["POST"])
def sol():
    interview_data = request.get_json(cache=False)
    return jsonify(stigfull(interview_data))


def stigfull(interview_data):
    p = 1
    q = 6
    output = []

    for interview in interview_data:
        print(len(interview["questions"]))
        lucky_number = interview["lucky"]
        max_rating = interview["maxRating"]
        questions = interview["questions"]
        for i in range(0, len(questions)):
            oldLower = questions[i]["lower"]
            oldUpper = questions[i]["upper"]
            newLower, newUpper = get_new_ques(
                oldLower, oldUpper, p, lucky_number, max_rating
            )
            questions[i]["lower"] = newLower
            questions[i]["upper"] = newUpper
            p, q = stig_process_gcd_new(max_rating, questions[: i + 1])
        output.append({"p": p, "q": q})

    return output
