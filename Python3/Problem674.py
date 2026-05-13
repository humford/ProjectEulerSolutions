import sys
import time


MODULUS = 1_000_000_000


class Variable:
    __slots__ = ("name",)

    def __init__(self, name):
        self.name = sys.intern(name)


class IExpression:
    __slots__ = ("left", "right")

    def __init__(self, left, right):
        self.left = left
        self.right = right


def parseExpression(expression):
    index = 0
    length = len(expression)

    def parse():
        nonlocal index
        if index >= length:
            raise ValueError("unexpected end of expression")

        if expression[index] == "I" and index + 1 < length and expression[index + 1] == "(":
            index += 2
            left = parse()
            if index >= length or expression[index] != ",":
                raise ValueError("expected comma")
            index += 1
            right = parse()
            if index >= length or expression[index] != ")":
                raise ValueError("expected closing parenthesis")
            index += 1
            return IExpression(left, right)

        start = index
        while index < length and expression[index].isalpha():
            index += 1
        if start == index:
            raise ValueError("expected variable")
        return Variable(expression[start:index])

    term = parse()
    if index != length:
        raise ValueError("trailing expression text")
    return term


def dereference(term, substitutions):
    while isinstance(term, Variable) and term.name in substitutions:
        term = substitutions[term.name]
    return term


def occursIn(name, term, substitutions):
    stack = [term]
    seenNodes = set()
    while stack:
        current = dereference(stack.pop(), substitutions)
        if isinstance(current, Variable):
            if current.name == name:
                return True
            continue

        identity = id(current)
        if identity in seenNodes:
            continue
        seenNodes.add(identity)
        stack.append(current.left)
        stack.append(current.right)

    return False


def unify(left, right):
    substitutions = {}
    stack = [(left, right)]

    while stack:
        a, b = stack.pop()
        a = dereference(a, substitutions)
        b = dereference(b, substitutions)

        if a is b:
            continue
        if isinstance(a, Variable) and isinstance(b, Variable) and a.name == b.name:
            continue

        if isinstance(a, Variable):
            if occursIn(a.name, b, substitutions):
                return None
            substitutions[a.name] = b
            continue

        if isinstance(b, Variable):
            if occursIn(b.name, a, substitutions):
                return None
            substitutions[b.name] = a
            continue

        stack.append((a.left, b.left))
        stack.append((a.right, b.right))

    return substitutions


def applyIOperator(left, right, modulus):
    if modulus is None:
        total = 1 + left + right
        return total * total + right - left

    total = (1 + left + right) % modulus
    return (total * total + right - left) % modulus


def evaluate(term, substitutions, modulus):
    memo = {}

    def value(current):
        current = dereference(current, substitutions)
        if isinstance(current, Variable):
            return 0

        identity = id(current)
        if identity not in memo:
            memo[identity] = applyIOperator(
                value(current.left),
                value(current.right),
                modulus,
            )
        return memo[identity]

    return value(term)


def leastSimultaneousValue(left, right, modulus=None):
    substitutions = unify(left, right)
    if substitutions is None:
        return 0
    return evaluate(left, substitutions, modulus)


def readExpressions(path="Files/p674_i_expressions.txt"):
    with open(path, encoding="utf-8") as file:
        return [parseExpression(line.strip()) for line in file if line.strip()]


def iEquationPairSum(expressions, modulus=MODULUS):
    total = 0
    for i in range(len(expressions)):
        for j in range(i + 1, len(expressions)):
            total += leastSimultaneousValue(expressions[i], expressions[j], modulus)
            total %= modulus
    return total


def runTests():
    a = parseExpression("I(x,I(z,t))")
    b = parseExpression("I(I(y,z),y)")
    c = parseExpression("I(I(x,z),y)")

    assert leastSimultaneousValue(a, b) == 23
    assert leastSimultaneousValue(a, c) == 0
    assert iEquationPairSum([a, b, c]) == 26


if __name__ == "__main__":
    sys.setrecursionlimit(1_000_000)
    runTests()
    start = time.time()
    answer = iEquationPairSum(readExpressions())
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
