import math
from typing import Tuple, List

from logic.location import Location


class Scan:
	def __init__(self, radius: float, angle: float):
		if angle < 0:
			raise ValueError("Scan cannot be lower 0")
		elif angle > 2 * math.pi:
			raise ValueError("Scan cannot be greater 2*pi")
		self._radius = radius
		self._angle = angle

	def get_radius(self) -> float:
		return self._radius

	def get_angle(self) -> float:
		return self._angle

	def calculate_energy_cost(self) -> float:
		return self._radius * self._angle
