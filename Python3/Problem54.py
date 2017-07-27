
words = open("/Users/henrywilliams/Documents/p054_poker.txt", "r")
words = words.read()
wordlist = sorted([x.replace("\"", "") for x in words.split(",")])

start = time.time()
answer = numberTriangleWords(wordlist)
elapsed = (time.time() - start)

print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
