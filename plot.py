#!/usr/bin/python

import curses
import argparse
import subprocess
from time import sleep

class Plot:
	def start(this, screen, args):
		screen_height, screen_width = screen.getmaxyx()

		i = 0
		scale_max = 1
		scale_min = 0

		values = []

		while True:
			i = i + 1

			# run command
			value = subprocess.check_output(args.command, shell=True)
			value = float(value.strip())

			# calc new scale
			if scale_max == 1:
				scale_max = value * 2
				scale_min = 0

			# adjust scale
			if value >= scale_max:
				scale_max = value * 1.2

			piece = scale_max / screen_height
			scale_value = int(value / piece)

			# invert because ncurses starts counting from top
			# minus one because position cannot exactely be screen_height
			scale_value = (screen_height - scale_value) - 1

			values.append(scale_value)

			if len(values) >= screen_width:
				values = values[1:]

			# draw graph
			screen.clear()

			# minus 2 because screen is printable until width-1 and bottom right is unusable?
			pos = screen_width-2
			j = len(values)-1

			while j >= 0:
				screen.addstr(values[j], pos, '-')
				j = j - 1
				pos = pos - 1

			screen.addstr(0, 0, 'running "{0}"'.format(args.command))
			screen.addstr(1, 0, 'Got value {0}, max scale {1}'.format(value, scale_max))
			screen.refresh()
			sleep(1)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Plot values in a graph')
	parser.add_argument('-n', default=2, required=False)
	parser.add_argument('command')
	args = parser.parse_args()

	plot = Plot()

	try:
		curses.wrapper(plot.start, args)
	except KeyboardInterrupt as e:
		pass
