def isLeapYear(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def daysInMonth(year, month):
    if month == 2:
        return 29 if isLeapYear(year) else 28
    if month in (4, 6, 9, 11):
        return 30
    return 31


def countFirstMonthSundays(startYear, endYear):
    weekday = 0
    count = 0

    for year in range(1900, endYear + 1):
        for month in range(1, 13):
            if year >= startYear and weekday == 6:
                count += 1
            weekday = (weekday + daysInMonth(year, month)) % 7

    return count


def runTests():
    assert isLeapYear(1900) is False
    assert isLeapYear(2000) is True
    assert daysInMonth(1904, 2) == 29


def solve():
    return countFirstMonthSundays(1901, 2000)


if __name__ == "__main__":
    runTests()
    print(solve())
