
from flask import jsonify, request
from routes import app
from datetime import datetime as dt
import datetime

# Input: "numbers": [2022, 1, 1, 0, 366]
# numbers[0] - year [2001, 2095]
# numbers[1:] - day of the year. only valid if is within [1,365]

# Part 1
# 96-character case-sensitive string, with every 8 characters
# corresponding to the month of the year starting with January.
# If all days: alldays,
# If only Sat, Sun: weekend,
# If only Mon-Fri: weekday.
# Else: "mtwtfss,", using an empty character ' ' for absent days
# Mon-Sun: [0, 6]


@app.route("/calendarDays", methods=["POST"])
def calendar_days():
    numbers = request.get_json()["numbers"]
    part1sol = sol1(numbers)
    return jsonify({
        "part1": part1sol,
        "part2": sol2(part1sol)})


def month_and_day_from_ordinal(year: int, day: int):
    startOfYear = dt(year, 1, 1)
    gregOrdinalYear = startOfYear.toordinal()
    # isLeapYear = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
    isLeapYear = ((year % 400 == 0) or (year % 100 != 0) and (year % 4 == 0))
    if ((isLeapYear and day <= 366) or
            (not isLeapYear and day <= 365)):
        gregOrdinalDay = gregOrdinalYear + day - 1
        actualDate = datetime.date.fromordinal(gregOrdinalDay)
        day = actualDate.weekday()
        month = actualDate.month
        return month, day
    else:
        print('invalid date')
        return -1, -1


def getPrint(dayList: list):
    if dayList == [1, 1, 1, 1, 1, 1, 1]:
        return "alldays"
    elif dayList == [1, 1, 1, 1, 1, 0, 0]:
        return "weekday"
    elif dayList == [0, 0, 0, 0, 0, 1, 1]:
        return "weekend"
    else:
        stringList = ['m', 't', 'w', 't', 'f', 's', 's']
        string = ""
        for i in range(0, 7):
            if dayList[i] == 1:
                string = string + stringList[i]
            else:
                string = string + " "
        return string


def sol1(input: list):
    year = input[0]
    monthsDict = dict()
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    for month in months:
        monthsDict[month] = [0, 0, 0, 0, 0, 0, 0]
    for day in input[1:]:
        if (day >= 0 and day <= 366):
            givenMonth, givenDay = month_and_day_from_ordinal(year, day)
            if (givenMonth != -1):
                monthsDict[givenMonth][givenDay] = 1
    sol = ""
    for month, dayList in monthsDict.items():
        sol += getPrint(dayList) + ","
    return(sol)


def sol2(input):
    add = 0
    for i in range(0, len(input)):
        if input[i] == " ":
            add = i
            break
    newYear = 2001 + add
    # split into list by ","
    inputList = input.split(",")
    ordinalDict = getOrdinalDict(newYear)
    days = []
    month = 1
    for string in inputList:
        if string == "alldays":
            days.extend(ordinalDict[month])
        if string == "weekday":
            days.extend(ordinalDict[month][0:5])
        if string == "weekend":
            days.extend(ordinalDict[month][5:7])
        else:
            for i in range(0, 7):
                if (i < len(string) and string[i] != " "):
                    days.append(ordinalDict[month][i])
        month += 1
    sol = [newYear] + days
    return sol


def getOrdinalDict(year):
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    dictOfMonths = dict()
    startOfYear = dt(year, 1, 1)
    gregOrdinalYear = startOfYear.toordinal()
    for month in months:
        d = dt(year, month, 1)  # datetime of first day of the month
        offset = d.weekday()  # which day of the week first day is, mon being 0
        ordinalDayNum = d.toordinal() - gregOrdinalYear + 1
        days = [0] * 7
        for i in range(0, 7):  # get days of one week
            oneDay = ordinalDayNum - offset + i + 7
            if (oneDay <= 0):
                oneDay = oneDay + 7
            days[i] = oneDay
        dictOfMonths[month] = days
    return dictOfMonths


# sol = sol1([2022, 1, 2, 8, 9, 15, 16, 22, 23, 29, 30])
# print(len(sol))
# input = "m      , t     ,weekend,       ,       ,       ,       ,       ,       ,       ,       ,       ,"
# print(sol2(input))
