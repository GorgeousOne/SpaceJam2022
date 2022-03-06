import numpy as np

class ScanAction:

	def __init__(self, direction: float, distance: float, angle: float):
		"""
		A class that tells the framework where to scan for spaceships.
		The amount of energy needed for a scan correlates to the size of the scanned area.
		:param direction: angle of the search direction (-pi to +pi)
		:param distance: the radius of the search area
		:param angle: angle that describes how narrow or wide the scanned area is (0 to 2*pi)
		"""
		self.direction = direction
		self.distance = distance
		self.angle = angle

class PilotAction:
	def __init__(self):
		"""
		A class that tells the framework to move the spaceship into some direction or shoot a rocket.
		"""
		self.acceleration = None
		self.shootAngle = None

	def move_spaceship_with_vec(self, acceleration: np.ndarray):
		"""
		Accelerates the spaceship with the given vector (without friction)
		Multiple accelerations will stack up or cancel each other out.
		The amount of energy for the acceleration correlates to the length of the vector.
		:param acceleration: impulse to accelerate the spaceship with
		:return:
		"""
		self.acceleration = acceleration

	def move_spaceship(self, direction: float, power: float):
		"""
		Accelerates the spaceship towards a direction with the given power (without friction)
		Multiple accelerations will stack up or cancel each other out.
		The amount of energy for the acceleration correlates to the used power.
		:param direction: direction to fly towards
		:param power: strength of the acceleration impulse
		"""
		self.acceleration = np.array([np.cos(direction), np.sin(direction)]) * power

	def shoot_rocket(self, direction: float):
		"""
		Shoots a rocket from the spaceship. This always costs the same amount of energy.
		:param direction: angle to shoot towards
		"""
		self.shootAngle = direction
