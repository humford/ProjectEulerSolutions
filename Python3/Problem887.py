import time


LIMIT = 7**10


def maximumNForQuestions(questionLimit, slack):
    if questionLimit <= slack + 1:
        return 1 << questionLimit

    shortLeafCount = questionLimit - slack - 1
    return (
        shortLeafCount
        + 2 * ((1 << slack) - 1) * (1 << shortLeafCount)
        + 2
    )


def Q(limit, slack):
    if slack == 0:
        return limit - 1

    questions = 0
    while maximumNForQuestions(questions, slack) < limit:
        questions += 1

    return questions


def sumQForSlack(limit, slack):
    if slack == 0:
        return limit * (limit - 1) // 2

    previousMaximum = 0
    questions = 0
    total = 0

    while previousMaximum < limit:
        questions += 1
        currentMaximum = min(maximumNForQuestions(questions, slack), limit)
        total += questions * (currentMaximum - previousMaximum)
        previousMaximum = currentMaximum

    return total


def solve():
    return sum(sumQForSlack(LIMIT, slack) for slack in range(8))


def runTests():
    assert Q(1, 0) == 0
    assert Q(7, 1) == 3
    assert Q(777, 2) == 10
    assert solve() == 39896187138661629


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
