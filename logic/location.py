import numpy as np

def wrap_to_pi(rad_angle):
	return (rad_angle + np.pi) % (2 * np.pi) - np.pi

class Location:

	def __init__(self, position: np.ndarray = np.zeros(2), rotation: float = 0, velocity: np.ndarray = np.zeros(2)):
		self._position = position.copy()
		self._rotation = wrap_to_pi(rotation)
		self._velocity = velocity.copy()

	def get_position(self) -> np.ndarray:
		return self._position

	def get_rotation(self) -> float:
		return self._rotation

	def get_direction(self) -> np.ndarray:
		return np.array([np.cos(self._rotation), np.sin(self._rotation)])

	def get_velocity(self) -> np.ndarray:
		return self._velocity

	def __repr__(self):
		return "(pos: " + str(self._position) + ", rot: " + str(round(np.rad2deg(self._rotation))) + ", vel: " + str(self._velocity) + ")"