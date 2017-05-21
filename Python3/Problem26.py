sequencelength = 0
num = 0

for i in range(1000, 1, -1):
    if sequencelength >= i:
    	break

    foundRemainders = [0 for x in range(i)]
    value = 1
    position = 0

    while foundRemainders[value] == 0 and value != 0:
    	foundRemainders[value] = position
    	value *= 10
    	value %= i
    	position += 1

    if position - foundRemainders[value] > sequencelength:
    	num = i
    	sequencelength = position - foundRemainders[value]

print(num, sequencelength)