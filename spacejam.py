from boxSpaceship import BoxSpaceship
from gui.framework import (Framework, main)


# from Box2D.examples.framework import (Framework, Keys, main)


class SpaceJam(Framework):
	name = "Space Jam"

	def __init__(self):
		super(SpaceJam, self).__init__()
		self.windowSize = 800
		self.window.set_size(self.windowSize, self.windowSize)
		self.window.set_caption("Space Jam")

		self.gameSize = 100
		self._create_battlefield()

		self.spaceShips = []
		self.spawn_ship()

	def _create_battlefield(self):
		self.world.gravity = (0.0, 0.0)

		border = self.world.CreateBody(position=(0, 0))
		border.CreateEdgeChain(
			[(-self.gameSize / 2, -self.gameSize / 2),
			 (-self.gameSize / 2, self.gameSize / 2),
			 (self.gameSize / 2, self.gameSize / 2),
			 (self.gameSize / 2, -self.gameSize / 2),
			 (-self.gameSize / 2, -self.gameSize / 2)]
		)
		self.setZoom((self.gameSize + 5) / 50)

	def spawn_ship(self):
		self.spaceShips.append(BoxSpaceship(self.world))


if __name__ == "__main__":
	app = main(SpaceJam)
