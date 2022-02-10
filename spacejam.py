from typing import Tuple

from Box2D import b2Color

from game.boxBorder import BoxBorder
from game.boxContactListener import BoxContactListener
from game.boxRocket import BoxRocket
from game.boxSpaceship import BoxSpaceship
from game.controllerHandler import ControllerHandler
from gui.framework import (Framework, main)


class SpaceJam(Framework):
	name = "Space Jam"

	def __init__(self):
		super(SpaceJam, self).__init__()

		self.windowSize = 800
		self.window.set_size(self.windowSize, self.windowSize)
		self.window.set_caption("Space Jam")
		self.spaceshipHandler = ControllerHandler()
		self.contactHandler = BoxContactListener(self.world)
		self.world.contactListener = self.contactHandler

		self.gameSize = 100
		self._create_battlefield()

		self.spawn_ship((-25, 0))
		self.spawn_ship((25, 0), b2Color(0.26, 0.53, 0.96))

	def Redraw(self):
		self.contactHandler.remove_bodies()
		self.border.display(self.renderer)

		for explosion in self.contactHandler.explosions:
			explosion.display(self.renderer)
		for rocket in self.contactHandler.rockets:
			rocket.display(self.renderer)
		for ship in self.contactHandler.spaceships:
			ship.display(self.renderer)

	def _create_battlefield(self):
		self.world.gravity = (0.0, 0.0)
		self.border = BoxBorder(self.world, self.gameSize, 1)
		self.setZoom((self.gameSize + 4) / 50)

	def spawn_ship(self, pos: Tuple[float, float] = (0, 0), fill: b2Color = b2Color(1, 0.73, 0)):
		self.contactHandler.add_spaceship(BoxSpaceship(self.world, 60, pos, fill))

	def Keyboard(self, key):
		if key == 32:
			for ship in self.contactHandler.spaceships:
				rocket = BoxRocket(self.world, ship)
				self.contactHandler.add_rocket(rocket)


if __name__ == "__main__":
	app = main(SpaceJam)
