from game.logic.scan import Scan


class SpaceAction:
	def __init__(self, rotation_angle: float = 0, scan: Scan = None):
		self.rotation_angle = rotation_angle
		self.scan = scan