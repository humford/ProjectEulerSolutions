import math
import time


DEFECTS = 20000
CHIPS = 1000000


def defectProbability(defects, chips):
    log_terms = []

    for double_defect_chips in range(defects // 2 + 1):
        single_defect_chips = defects - 2 * double_defect_chips
        empty_chips = chips - single_defect_chips - double_defect_chips

        if empty_chips < 0:
            continue

        log_terms.append(
            math.lgamma(chips + 1)
            + math.lgamma(defects + 1)
            - math.lgamma(double_defect_chips + 1)
            - math.lgamma(single_defect_chips + 1)
            - math.lgamma(empty_chips + 1)
            - double_defect_chips * math.log(2)
            - defects * math.log(chips)
        )

    maximum = max(log_terms)
    no_triple_probability = math.exp(maximum) * sum(
        math.exp(term - maximum) for term in log_terms
    )

    return 1 - no_triple_probability


def runTests():
    assert format(defectProbability(3, 7), ".10f") == "0.0204081633"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = format(defectProbability(DEFECTS, CHIPS), ".10f")
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
