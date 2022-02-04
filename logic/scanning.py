from typing import Tuple, List


class Scan:
	def __init__(self, radius: float, angle: float):
		self._radius = radius
		self._angle = angle

	def get_radius(self):
		return self._radius

	def get_angle(self):
		return self._angle

class RocketScan:
	def __init__(self, position: Tuple[float, float], velocity: float):
		self._position = position
		self._velocity = velocity

class ScanResult:
	def __init__(self, located_rockets: List[RocketScan]):
		self._located_rockets = located_rockets

	def get_located_rockets(self) -> List[RocketScan]:
		return self._located_rockets
