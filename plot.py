#!/usr/bin/python

import curses
import argparse
import subprocess
from time import sleep

class Plot:
	def start(self, screen, args):
		screen_height, screen_width = screen.getmaxyx()

		i = 0
		scale_max = 1
		scale_min = 0

		values = []

		pw = PlotWindow(screen)

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

			values.append(value)

			if len(values) >= screen_width:
				values = values[1:]

			pw.draw_graph(scale_min, scale_max, values)

			screen.addstr(0, 0, 'running "{0}"'.format(args.command))
			screen.addstr(1, 0, 'Got value {0}, max scale {1}'.format(value, scale_max))
			screen.refresh()
			sleep(1)

class PlotWindow:
	screen_height = 0
	screen_width = 0
	screen = False

	def __init__(self, screen):
		self.screen_height, self.screen_width = screen.getmaxyx()
		self.screen = screen

	def draw_graph(self, scale_min, scale_max, values):
		self.screen.clear()

		# minus 2 because screen is printable until width-1 and bottom right is unusable?
		pos = self.screen_width-2
		j = len(values)-1

		piece = scale_max / self.screen_height

		while j >= 0:
			value = values[j]
			scale_value = int(value / piece)

			# invert because ncurses starts counting from top
			# minus one because position cannot exactely be screen_height
			scale_value = (self.screen_height - scale_value) - 1

			self.screen.addstr(scale_value, pos, '-')
			j = j - 1
			pos = pos - 1


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
