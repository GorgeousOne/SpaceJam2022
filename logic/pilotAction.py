
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

	def scan_area(self, radius: float, direction: float, angle: float, ):
		self.scan_action = {
			"radius": radius,
			"direction": direction,
			"angle": angle
		}

	def shoot_rocket(self, angle: float):
		self.shoot_action = {
			"angle": angle
		}
