years = {}
for x in range(1901, 2001):
	if (x % 4 == 0) and ((not x % 100 == 0) or (x % 400 == 0)):
		years[x] = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	else:
		years[x] = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
numdays = 0
numsundays = 0
for year in years:
	for month in years[year]:
		if numdays % 7 == 0:
			numsundays += 1
		numdays += month
print(numsundays)