import pyglet
from Box2D import b2Color

from game.boxBorder import BoxBorder
from game.boxRocket import BoxRocket
from game.boxSpaceship import BoxSpaceship
from game.controllerHandler import ControllerHandler
from gui.framework import (Framework, main, Keys)


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
		self.bullets = []

		self.spawn_ship()
		self.spaceshipHandler = ControllerHandler()

	def Redraw(self):
		self.border.display(self.renderer)
		for bullet in self.bullets:
			bullet.display(self.renderer)

		for ship in self.spaceships:
			ship.display(self.renderer)

	def _create_battlefield(self):
		self.world.gravity = (0.0, 0.0)
		self.border = BoxBorder(self.world, self.gameSize, 1)
		self.setZoom((self.gameSize + 4) / 50)

	def spawn_ship(self):
		self.spaceships.append(BoxSpaceship(self.world, color=b2Color(1, 0.73, 0)))

	def Keyboard(self, key):
		if key == 32:
			for ship in self.spaceships:
				self.bullets.append(BoxRocket(self.world, ship))


if __name__ == "__main__":
	app = main(SpaceJam)
