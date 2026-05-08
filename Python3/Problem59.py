import itertools
import time
from pathlib import Path


def readCiphertext():
    path = Path(__file__).resolve().parents[1] / "Files" / "p059_cipher.txt"
    return [int(value) for value in path.read_text().strip().split(",")]


def decrypt(ciphertext, key):
    return "".join(chr(value ^ key[index % len(key)]) for index, value in enumerate(ciphertext))


def englishScore(text):
    common_words = [" the ", " and ", " of ", " to ", " in ", " that ", " is ", " be "]
    score = sum(text.count(word) * 20 for word in common_words)
    score += sum(char in " etaoinshrdluETAOINSHRDLU" for char in text)
    score -= sum(ord(char) < 32 or ord(char) > 126 for char in text) * 100
    return score


def findMessage(ciphertext):
    best_score = None
    best_key = None
    best_message = None

    for key_chars in itertools.product(range(ord("a"), ord("z") + 1), repeat=3):
        message = decrypt(ciphertext, key_chars)
        score = englishScore(message)
        if best_score is None or score > best_score:
            best_score = score
            best_key = key_chars
            best_message = message

    return "".join(chr(char) for char in best_key), best_message


def asciiSum(text):
    return sum(ord(char) for char in text)


def runTests():
    assert decrypt([9, 7, 15], [ord("a")]) == "hfn"
    assert asciiSum("ABC") == 198


if __name__ == "__main__":
    runTests()
    start = time.time()
    key, message = findMessage(readCiphertext())
    answer = asciiSum(message)
    elapsed = time.time() - start

    print("Key " + key)
    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
