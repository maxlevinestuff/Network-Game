#Code that is common to a few places

import random as ran

#takes a range, list, or single variable, and turns it to a list
def turn_to_list(list_or_other):
	if isinstance(list_or_other, range):
		list_or_other = [*list_or_other]
	if not isinstance(list_or_other, list):
		list_or_other = [list_or_other]
	return list_or_other
#chooses randomly among a range, list, or single variable
def turn_to_list_and_choose(list_or_other):
	return ran.choice(turn_to_list(list_or_other))