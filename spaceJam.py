import math

import pyglet
from Box2D import b2Vec2, b2Color

from game.boxBackground import BoxBackground
from game.boxBorder import BoxBorder
from game.boxContactListener import BoxContactListener
from game.boxRocket import BoxRocket
from game.gameHandler import GameHandler
from game.pilotHandler import PilotHandler
from gui.pygletFramework import PygletFramework
from logic.pilots.afkPilot import AfkPilot
from logic.pilots.circlePilot import CirclePilot


class SpaceJam(PygletFramework):
	name = "Space Jam"

	def __init__(self):
		super(SpaceJam, self).__init__()

		self.windowSize = 600
		self.window.set_size(self.windowSize, self.windowSize)
		self.window.set_caption("Space Jam")
		self.gameSize = 100
		self.frameCount = 0

		self.contactHandler = BoxContactListener(self.world)
		self.world.contactListener = self.contactHandler

		self.gameHandler = GameHandler(self.world, self.contactHandler, self.gameSize)
		# spaceship svg model currently has size 5
		self.pilotHandler = PilotHandler(self.gameHandler, self.gameSize, 5)

		self._create_game_field()
		self.pilotHandler.add_cmd_line_pilots()

	def Redraw(self):
		self.frameCount += 1

		if self.frameCount % (self.settings.hz // 5) == 0:
			self.gameHandler.update()

		self.contactHandler.remove_bodies()

		# try to keep the amount of layers low :P
		for ship in self.contactHandler.spaceships:
			ship.display(self.renderer, 0)
		for explosion in self.contactHandler.explosions:
			explosion.display(self.renderer, 1)
		for scan in self.contactHandler.scans:
			scan.display(self.renderer, 1)
		for rocket in self.contactHandler.rockets:
			rocket.display(self.renderer, 1)

		self.border.display(self.renderer, 0)
		self.background.display(self.renderer, 2, self.frameCount)

	def _create_game_field(self):
		self.world.gravity = (0.0, 0.0)
		self.border = BoxBorder(self.world, self.gameSize, 1)
		self.background = BoxBackground(self.gameSize)

		self.renderer.setZoom((self.gameSize + 4) / 50)
		self.renderer.setCenter(b2Vec2(self.gameSize / 2, self.gameSize / 2))

	def Keyboard(self, key):
		if key == 32:
			for ship in self.contactHandler.spaceships:
				heading = b2Vec2(math.cos(ship.body.angle), math.sin(ship.body.angle)) * 30
				rocket = BoxRocket(self.world, ship, heading)
				self.contactHandler.add_rocket(rocket)


if __name__ == "__main__":
	SpaceJam().run()
	pyglet.app.run()
