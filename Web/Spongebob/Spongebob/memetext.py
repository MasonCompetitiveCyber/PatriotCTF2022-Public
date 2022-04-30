# source: https://www.geeksforgeeks.org/spongebob-mocking-text-generator-python/
import random
import sys

def spongemock(input_text):
	output_text = ""
	for char in input_text:
		if char.isalpha():
			if random.random() > 0.5:
				output_text += char.upper()
			else:
				output_text += char.lower()
		else:
			output_text += char

	return output_text

if __name__=="__main__":
	input_text1 = sys.argv[1]
	print(spongemock(input_text1))