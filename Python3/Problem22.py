words = open("/Users/henrywilliams/Documents/p022_names.txt", "r")
words = words.read()
wordlist = sorted([x.replace("\"", "") for x in words.split(",")])
total = 0
for word in wordlist:
	total += sum([ord(l)-64 for l in list(word)]) * (wordlist.index(word) + 1)
print(total)