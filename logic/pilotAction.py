
class PilotAction:
	def __init__(self):
		self.move_action = None
		self.scan_action = None
		self.shoot_action = None

	def move_spaceship(self, direction: float, power: float):
		self.move_action = {
			"direction": direction,
			"power": power
		}

	def scan_area(self, direction: float, angle: float, radius: float):
		self.scan_action = {
			"direction": direction,
			"angle": angle,
			"radius": radius
		}

	def shoot_rocket(self, angle: float):
		self.shoot_action = {
			"angle": angle
		}
