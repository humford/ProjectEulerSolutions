coins = [200, 100, 50, 20, 10, 5, 2, 1]

def coinSum(n, coin):
	ways = 0
	for x in range(n, -1, -coins[coin]):
		if coins[coin] == 2:
			ways += 1
		else:
			ways += coinSum(x, coin+1)
	return ways

print(coinSum(200, 0))