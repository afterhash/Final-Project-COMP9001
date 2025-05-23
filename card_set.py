import random
import os

CARD_SUIT = ("♠", "♥", "♦", "♣")
CARD_SIZE = ("A", "2", "3", "4", "5", "6", "7",
"8", "9", "10", "J", "Q", "K")


def init_random():
	seed = int.from_bytes(os.urandom(4), byteorder='big')
	random.seed(seed)


class Card:
	def __init__(self, size: str, suit: str):
		if size in CARD_SIZE and suit in CARD_SUIT:
			self.size = size
			self.suit = suit
		else:
			raise ValueError("Card init failed")

	def get_size(self):
		return self.size

	def get_suit(self):
		return self.suit

	def __str__(self):
		return f'This card is {self.suit}{self.size}'


class CardSet:
	def __init__(self):
		self.num_card = 52
		self.card_list = []
		for suit in CARD_SUIT:
			for size in CARD_SIZE:
				self.card_list.append(Card(size, suit))
		self.card_sequence = self.shuffle()

	# Fisher-Yates Shuffle Algorithm
	def shuffle(self):
		init_random()
		sequence = list(range(0, self.num_card))
		# 51 -> 0
		for i in range(self.num_card - 1, -1, -1):
			j = random.randint(0, i)
			temp = sequence[i]
			sequence[i] = sequence[j]
			sequence[j] = temp
		return sequence

	def isEmpty(self):
		return self.num_card == 0

	def get_card(self):
		if self.num_card <= 0:
			raise ValueError("CardSet is Empty.")
		index = self.card_sequence.pop()
		self.num_card -= 1
		return self.card_list[index]


if __name__ == '__main__':
	cs = CardSet()
	for i in range(10):
		print(cs.get_card())