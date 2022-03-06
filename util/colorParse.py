from typing import Tuple

from Box2D import b2Color


def hex_to_rgb(hex_string: str):
	try:
		r = int(hex_string[1:3], 16)
		g = int(hex_string[3:5], 16)
		b = int(hex_string[5:7], 16)
		return r, g, b
	except ValueError:
		print("Could not read HEX color: \"" + hex_string + "\".")
		return 255, 255, 255

def rgb_to_b2color(triple: Tuple):
	return b2Color(triple[0] / 255, triple[1] / 255, triple[2] / 255)

