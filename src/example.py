#!/usr/bin/env python3

import rulegenerator
from random import randint

if __name__ == '__main__':
	generations = 500
	width = 501
	
	rule = randint(0, 255)
	
	init_config = randint(0, 32)
	init_config = bin(init_config)[2:]
	
	grid = rulegenerator.generate_rule_wrap(generations, init_config, rule, width)
	
	print("Writing to image...")
	
	rulegenerator.to_image(grid, './examples/' + str(rule) + '.png')
	
	print("Done.")
	