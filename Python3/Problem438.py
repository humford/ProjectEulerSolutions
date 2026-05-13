from itertools import combinations
import math
import time


EPSILON = 1e-9


def elementarySums(values):
    return [1] + [
        sum(math.prod(combination) for combination in combinations(values, size))
        for size in range(1, len(values) + 1)
    ]


class LinearSystem:
    def __init__(self, lower=None, upper=None, equal=None):
        self.lower = lower or []
        self.upper = upper or []
        self.equal = equal or []

    def addConstraint(self, coefficients):
        coefficients = list(coefficients)
        eliminatedCoefficient = -coefficients.pop()
        if abs(eliminatedCoefficient) < EPSILON:
            self.equal.append(coefficients)
            return

        normalized = [coefficient / eliminatedCoefficient for coefficient in coefficients]
        if eliminatedCoefficient > EPSILON:
            self.lower.append(normalized)
        else:
            self.upper.append(normalized)


def difference(left, right):
    return [a - b for a, b in zip(left, right)]


def eliminateOne(system):
    result = LinearSystem()
    for equality in system.equal:
        result.addConstraint(equality)
    for lower in system.lower:
        for upper in system.upper:
            result.addConstraint(difference(lower, upper))
    return result


def evaluateLinear(coefficients, values):
    return coefficients[0] + sum(
        coefficients[index + 1] * value
        for index, value in enumerate(values)
    )


def tightFloor(value):
    return math.floor(value + EPSILON)


def tightCeil(value):
    return math.ceil(value - EPSILON)


def inferredRange(system, prefix):
    for equality in system.equal:
        if evaluateLinear(equality, prefix) > EPSILON:
            return 1, 0

    lower = -10**18
    upper = 10**18
    for constraint in system.lower:
        lower = max(lower, tightCeil(evaluateLinear(constraint, prefix)))
    for constraint in system.upper:
        upper = min(upper, tightFloor(evaluateLinear(constraint, prefix)))
    return lower, upper


def validIntegerEndpoint(degree, prefix, lastValue):
    coefficients = prefix + [lastValue]
    for point in range(1, degree + 2):
        value = 1
        for index, coefficient in enumerate(coefficients):
            value = point * value + (coefficient if index % 2 else -coefficient)

        if value == 0:
            derivative = degree
            for index in range(degree - 1):
                coefficient = coefficients[index] if index % 2 else -coefficients[index]
                derivative = point * derivative + (degree - index - 1) * coefficient
            if (degree + point) % 2 == 1:
                if derivative >= 0:
                    return False
            elif derivative <= 0:
                return False
    return True


class PolynomialCounter:
    def __init__(self, degree, directDepth=2):
        self.degree = degree
        self.directDepth = directDepth
        self.lower = elementarySums(range(1, degree + 1))
        self.upper = elementarySums(range(2, degree + 2))
        self.systems = [None] * (degree + 2)
        self.prefix = []
        self.count = 0
        self.absoluteSum = 0

        constraints = []
        for point in range(1, degree + 2):
            coefficients = [0.0] * (degree + 1)
            coefficients[degree] = 1.0
            for index in range(degree - 1, -1, -1):
                coefficients[index] = -point * coefficients[index + 1]
            if point % 2 == 1:
                coefficients = [-coefficient for coefficient in coefficients]
            constraints.append(coefficients)

        self.systems[degree + 1] = LinearSystem(equal=constraints)
        for index in range(degree, directDepth, -1):
            self.systems[index] = eliminateOne(self.systems[index + 1])

    def search(self, index):
        lower = self.lower[index]
        upper = self.upper[index] - 1
        if index > self.directDepth:
            inferredLower, inferredUpper = inferredRange(self.systems[index], self.prefix)
            lower = max(lower, inferredLower)
            upper = min(upper, inferredUpper)
        if lower > upper:
            return

        if index == self.degree:
            while lower <= upper and not validIntegerEndpoint(self.degree, self.prefix, lower):
                lower += 1
            while lower <= upper and not validIntegerEndpoint(self.degree, self.prefix, upper):
                upper -= 1
            if lower > upper:
                return

            count = upper - lower + 1
            self.count += count
            self.absoluteSum += count * (lower + upper) // 2 + sum(self.prefix) * count
            return

        for value in range(lower, upper + 1):
            self.prefix.append(value)
            self.search(index + 1)
            self.prefix.pop()

    def solve(self):
        self.search(1)
        return self.count, self.absoluteSum


def tupleCount(n):
    return PolynomialCounter(n).solve()[0]


def coefficientAbsoluteSum(n):
    return PolynomialCounter(n).solve()[1]


def runTests():
    assert tupleCount(4) == 12
    assert coefficientAbsoluteSum(4) == 2087


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = coefficientAbsoluteSum(7)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
