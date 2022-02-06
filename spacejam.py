from Box2D import b2Color

from game.boxBorder import BoxBorder
from game.boxSpaceship import BoxSpaceship
from game.spaceshipHandler import SpaceshipHandler
from gui.framework import (Framework, main)


class SpaceJam(Framework):
	name = "Space Jam"

	def __init__(self):
		super(SpaceJam, self).__init__()

		self.windowSize = 800
		self.window.set_size(self.windowSize, self.windowSize)
		self.window.set_caption("Space Jam")

		self.gameSize = 100
		self._create_battlefield()

		self.spaceships = []
		self.spawn_ship()
		self.spaceshipHandler = SpaceshipHandler()

	def Redraw(self):
		# super(SpaceJam, self).Redraw()
		self.border.display(self.renderer)
		for ship in self.spaceships:
			ship.display(self.renderer)

	def _create_battlefield(self):
		self.world.gravity = (0.0, 0.0)
		self.border = BoxBorder(self.world, self.gameSize, 1)
		self.setZoom((self.gameSize + 5) / 50)

	def spawn_ship(self):
		self.spaceships.append(BoxSpaceship(self.world, color=b2Color(1, 0.73, 0)))


if __name__ == "__main__":
	app = main(SpaceJam)
