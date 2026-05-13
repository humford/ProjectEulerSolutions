import time
from collections import deque


ALPHABET = ("A", "E", "F", "R")
KEYWORDS = ("FREE", "FARE", "AREA", "REEF")


class KeywordAutomaton:
    def __init__(self, words):
        self.edges = [{}]
        self.failures = [0]
        self.outputs = [0]

        for index, word in enumerate(words):
            self.addWord(word, index)

        self.buildFailures()
        self.transitions = self.buildTransitions()

    def addWord(self, word, index):
        state = 0
        for letter in word:
            if letter not in self.edges[state]:
                self.edges[state][letter] = len(self.edges)
                self.edges.append({})
                self.failures.append(0)
                self.outputs.append(0)
            state = self.edges[state][letter]
        self.outputs[state] |= 1 << index

    def buildFailures(self):
        queue = deque(self.edges[0].values())
        while queue:
            state = queue.popleft()
            self.outputs[state] |= self.outputs[self.failures[state]]

            for letter, child in self.edges[state].items():
                fallback = self.failures[state]
                while fallback and letter not in self.edges[fallback]:
                    fallback = self.failures[fallback]
                self.failures[child] = self.edges[fallback].get(letter, 0)
                queue.append(child)

    def buildTransitions(self):
        transitions = []
        for state in range(len(self.edges)):
            row = []
            for letter in ALPHABET:
                current = state
                while current and letter not in self.edges[current]:
                    current = self.failures[current]
                row.append(self.edges[current].get(letter, 0))
            transitions.append(row)
        return transitions


def keywordWordCount(length):
    automaton = KeywordAutomaton(KEYWORDS)
    fullMask = (1 << len(KEYWORDS)) - 1
    stateCount = len(automaton.edges)
    maskCount = 1 << len(KEYWORDS)

    counts = [[0] * maskCount for _ in range(stateCount)]
    counts[0][0] = 1

    for _ in range(length):
        nextCounts = [[0] * maskCount for _ in range(stateCount)]
        for state in range(stateCount):
            for mask, count in enumerate(counts[state]):
                if count == 0:
                    continue
                for nextState in automaton.transitions[state]:
                    output = automaton.outputs[nextState]
                    if output & mask:
                        continue
                    nextCounts[nextState][mask | output] += count
        counts = nextCounts

    return sum(counts[state][fullMask] for state in range(stateCount))


def runTests():
    assert keywordWordCount(9) == 1
    assert keywordWordCount(15) == 72_863


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = keywordWordCount(30)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
