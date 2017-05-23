import time
import math

def triangleNumber(n):
    return n * (n + 1) / 2

def testTriangular(n):
    n = float(n)
    n = (math.sqrt(8 * n + 1) - 1) / 2
    return n.is_integer()

def wordValue(word):
	val = 0
	for x in word:
		val += ord(x) - 64
	return val

def numberTriangleWords(words):
	numTriangle = 0
	for word in words:
		if testTriangular(wordValue(word)):
			numTriangle += 1
	return numTriangle

words = open("/Users/henrywilliams/Documents/p042_words.txt", "r")
words = words.read()
wordlist = sorted([x.replace("\"", "") for x in words.split(",")])

start = time.time()
answer = numberTriangleWords(wordlist)
elapsed = (time.time() - start)

print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")