import math
import time

def collatzSequence(n):
	sequence = [n]
	while n != 1:
		if n % 2 == 0:
			n = n / 2
		else:
			n = 3*n + 1
		sequence.append(n)
	return sequence

def findLongest(max):
	l = 0
	start = 0
	for x in range(max,1,-1):
		seqlen = len(collatzSequence(x))
		if seqlen > l:
			l = seqlen
			start = x
			print start, l
	return start

start = time.time()
startingnumber = findLongest(int(raw_input("Under: ")))
elapsed = (time.time() - start)

print "found %s in %s seconds" % (startingnumber, elapsed)