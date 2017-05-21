from num2words import num2words

def numberOfLetters(num):
    word = num2words(num)
    concat_word = word.replace(" ", "")
    concat_word_final = concat_word.replace("-", "")
    return len(concat_word_final)

total = 0
for n in range(1, 1001):
	total += numberOfLetters(n)
print(total)

