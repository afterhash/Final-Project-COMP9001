import card_set
from itertools import permutations

def show_card(a: card_set.Card, b, c, d) -> str:
	'''
	Display card beautifdully.

	Parameters:
		a (Card): Four cards in total.
		b (Card): Four cards in total.
		c (Card): Four cards in total.
		d (Card): Four cards in total.

	Returns:
		str: beautified card string.
	'''
	a_s = a.get_suit() + a.get_size() + ' ' if a.get_size() != '10' \
			else a.get_suit() + a.get_size()
	b_s = b.get_suit() + b.get_size() + ' ' if b.get_size() != '10' \
			else b.get_suit() + b.get_size()
	c_s = c.get_suit() + c.get_size() + ' ' if c.get_size() != '10' \
			else c.get_suit() + c.get_size()
	d_s = d.get_suit() + d.get_size() + ' ' if d.get_size() != '10' \
			else d.get_suit() + d.get_size()
	return f"""
  |-----||-----|
  |  {a_s}||  {b_s}|
  |     ||     |
  |-----||-----|
|-----||-----|
|  {c_s}||  {d_s}|
|     ||     |
|-----||-----|
	"""


def solve_24(nums):
	"""
	Solve the 24 points problem.

	Parameters:
		nums (list[int]): The numbers on cards.

	Returns:
		solutions (list[str]): All arithmetic expressions of the possible solution.
	"""
	if len(nums) != 4:
		return []
	
	ops = ['+', '-', '*', '/']
	solutions = set()  # avoid duplicate solutions

	# traverse all the numerical permutations
	for a, b, c, d in permutations(nums):
		# traverse all combinations of operators
		for op1 in ops:
			for op2 in ops:
				for op3 in ops:
					# try five different combinations of parentheses
					expressions = [
						f"(({a}{op1}{b}){op2}{c}){op3}{d}",  # ((a op1 b) op2 c) op3 d
						f"({a}{op1}({b}{op2}{c})){op3}{d}",  # (a op1 (b op2 c)) op3 d
						f"({a}{op1}{b}){op2}({c}{op3}{d})",  # (a op1 b) op2 (c op3 d)
						f"{a}{op1}(({b}{op2}{c}){op3}{d})",  # a op1 ((b op2 c) op3 d)
						f"{a}{op1}({b}{op2}({c}{op3}{d}))"   # a op1 (b op2 (c op3 d))
					]
					for expr in expressions:
						# calculate the result
						try:
							if abs(eval(expr) - 24) < 1e-6:
								# TODO some brackets can be deleted
								solutions.add(expr)

						except ZeroDivisionError:
							continue
	
	return list(solutions)


def is_valid_expression(expr, nums):
	"""
	Check whether the expression only contains +-*/() and the exact numbers in nums

	Parameters:
		expr (str): the expression
		nums (list[int]): The numbers.

	Returns:
		True(valid) or False(invalid)
	"""
	# valid symbols
	allowed_chars = {'+', '-', '*', '/', '(', ')', ' '}
	numbers_in_expr = []
	
	# check validity of each char
	i = 0
	while i < len(expr):
		char = expr[i]
		# invalid char
		if char not in allowed_chars and not char.isdigit():
			return False
		elif char.isdigit():
			num = int(char)
			while i < len(expr) - 1 and expr[i + 1].isdigit():
				num = num * 10 + int(expr[i + 1])
				i += 1
			numbers_in_expr.append(num)
		
		i += 1
	
	# check numbers
	if sorted(numbers_in_expr) != sorted(nums):
		return False
	
	return True


if __name__ == '__main__':
	print('''
Welcome to the 24-Point Game.

* 24-Point Game Rules *
1.Draw 4 random cards (A=1, J/Q/K=11/12/13).
2.Use +, -, *, / and parentheses to make 24 with all 4 numbers.
3.Each number must be used exactly once.

Example: 3, 3, 8, 8 → 8 / (3 - (8 / 3)) = 24
''')
	# times of this game
	while True:
		game_time = input("How many times do you want to play?([number] / 'random')") 
		if game_time.strip().lower() == 'random':
			card_set.init_random()
			game_time = card_set.random.randint(1, 10)
			break
		elif game_time.isdigit():
			game_time = int(game_time)
			break
		else:
			print(f"ValueError: {game_time}")
	
	# start game
	cs = card_set.CardSet()
	num_problem_solved = 0
	dict_size_num = {
	'A': 1, '2': 2, '3': 3, '4': 4, '5': 5,
	'6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
	'J': 11, 'Q': 12, 'K': 13
	}
	print("Game Start :)")
	num_played_times = 0
	while True:
		flag_continue_playing = True
		num_played_times += 1

		print(f"{num_played_times} / {game_time}:")
		playing_cards = []
		playing_nums = []
		solutions = []
		# get cards
		while True:
			# get random 4 cards
			for j in range(4):
				if cs.isEmpty():
					cs = card_set.CardSet()
				
				playing_cards.append(cs.get_card())

			playing_nums = [dict_size_num.get(k.get_size()) for k in playing_cards]
			# loop until there are solutions 
			print("Plaese wait...")
			solutions = solve_24(playing_nums)
			if solutions:
				break
		
		while True:
			ans = input("Ready?[y/n]:")
			if ans == 'y':
				break

		# show card
		print(show_card(playing_cards[0], playing_cards[1] \
						, playing_cards[2], playing_cards[3]))
		
		# input answer
		while True:
			print("Got any idea?(input arithmetic expression or no idea or quit):")
			print("Note that power(**) and factorial(!) is excluded.")
			print("Note that use 1 for A, 11 for J, 12 for Q and 13 for K")
			expression = input().strip().lower()
			
			if expression == 'quit':
				flag_continue_playing = False
				break

			if expression == 'no idea':
				expression = '-'.join([str(x) for x in playing_nums])
			
			if is_valid_expression(expression, playing_nums):
				break
			else:
				print("Invalid expression!")
				print()
				continue
		
		# not quit
		if flag_continue_playing:
			if abs(eval(expression) - 24) < 1e-6:
				print("Good Job!")
				print()
				num_problem_solved += 1
			else:
				print("Try harder!")
				print("Solutions:")
				for i in solutions:
					print("   ", i)
				print()
		
		# last turn
		if num_played_times == game_time:
			flag_continue_playing = False

		# end of game
		if not flag_continue_playing:
			print(f"You have worked out {num_problem_solved} / {num_played_times} problems.")
			print("Thank you for your time!")
			break
		

