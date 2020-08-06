import time
import math
import numpy as np
import collections

hands = open("../Files/p054_poker.txt", "r")
hands = hands.read()
handlist = hands.split("\n")

cardvals = {"1":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "T":10, "J":11, "Q":12, "K":13, "A":14}
handvals = {"HC":1, "OP":2, "TP":3, "TK":4, "ST":5, "FL":6, "FH":7, "FK":8, "SF":9, "RF":10}
# Spades, Clubs, Diamonds, Hearts

def is_straight(player_card_values):
	return (sum(np.diff(sorted(player_card_values)) == 1) >= 4)

def is_flush(player_hand):
	suit = player_hand[0][1]
	return len(player_hand) == len([card for card in player_hand if suit in card])

def hand_value(player_hand):
	handval = "HC"
	rankval = 0
	card_values = []
	for i in range(5):
		card_values.append(cardvals[player_hand[i][0]])
	card_values = sorted(card_values, reverse = True)

	# Count instances of all cards
	cnt = dict(collections.Counter(card_values))
	sorted_cnt = {k: v for k, v in sorted(cnt.items(), key=lambda item: item[1], reverse = True)}
	
	# One Pair
	if max(cnt.values()) == 2:
		# Two Pairs
		if sorted(cnt.values(), reverse = True)[1] == 2:
			handval = "TP"
			rankval = next(iter(sorted_cnt))
		else:
			handval = "OP"
			rankval = next(iter(sorted_cnt))

	# Three of a Kind
	if max(cnt.values()) == 3:
		handval = "TK"
		rankval = next(iter(sorted_cnt))

	# Straight
	if is_straight(card_values):
		handval = "ST"
		rankval = max(card_values)

	# Flush
	if is_flush(player_hand):
		# Straight Flush
		if handval == "ST":
			handval = "SF"
			rankval = max(card_values)
		else:
			handval = "FL"
			rankval = max(card_values)

	# Full House
	if max(cnt.values()) == 3:
		if sorted(cnt.values(), reverse = True)[1] == 2:
			handval = "FH"
			rankval = next(iter(sorted_cnt))

	# Four of a Kind
	if max(cnt.values()) == 4:
		handval = "FK"
		rankval = next(iter(sorted_cnt))

	# Royal Flush
	if handval == "SF":
		if max(card_values) == 14:
			handval = "RF"
			rankval = 14

	return handval, card_values, rankval

def find_winner(player1, player2):
	hand_player1, card_values_player1, rankval_player1 = hand_value(player1)
	hand_player2, card_values_player2, rankval_player2 = hand_value(player2)

	if handvals[hand_player1] > handvals[hand_player2]:
		return 1
	elif handvals[hand_player1] < handvals[hand_player2]:
		return 2
	else:
		if rankval_player1 > rankval_player2:
			return 1
		elif rankval_player1 < rankval_player2:
			return 2
		else:
			if max(card_values_player1) > max(card_values_player2):
				return 1
			elif max(card_values_player1) < max(card_values_player2):
				return 2

def count_wins(handlist):
	one_wins = 0
	two_wins = 0

	for hand in handlist:
		cards = hand.split(" ")
		player1 = cards[:5]
		player2 = cards[5:]

		if find_winner(player1, player2) == 1:
			one_wins += 1
		else:
			two_wins += 1
	return one_wins, two_wins

start = time.time()
wins = count_wins(handlist)
elapsed = (time.time() - start)

print("Player_1 won " + str(wins[0]) + " games and Player_2 won " + str(wins[1]) + " games in " + str(elapsed) + " seconds.")
