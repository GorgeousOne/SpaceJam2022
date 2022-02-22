import math
from typing import List

import pyglet
from Box2D import b2Vec2

from game.boxBackground import BoxBackground
from game.boxBorder import BoxBorder
from game.boxContactListener import BoxContactListener
from game.boxRocket import BoxRocket
from game.gameHandler import GameHandler
from render.pygletFramework import PygletFramework


class GameSimulation(PygletFramework):
	name = "Space Jam"

	def __init__(self, window: pyglet.window.Window, background: BoxBackground, pilot_classes: List, game_over_callback = None):
		super(GameSimulation, self).__init__(window)

		self.background = background
		self.gameOverCallback = game_over_callback
		self.gameSize = 100
		self.frameCount = 0
		# spaceship svg model currently has size 5
		self.spaceshipSize = 5

		self.contactHandler = BoxContactListener(self.world)
		self.world.contactListener = self.contactHandler
		self.gameHandler = GameHandler(self.world, self.contactHandler, self.gameSize)
		self._create_game_field()
		for pilot in pilot_classes:
			self.gameHandler.spawn_spaceship(pilot(self.gameSize, self.spaceshipSize))

	def set_frame_count(self, frame_count: int):
		self.frameCount = frame_count

	def cancel(self):
		super().cancel()

	def Redraw(self):
		if len(self.contactHandler.spaceships) < 2:
			if self.gameOverCallback:
				self.gameOverCallback()
			return

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
		self.renderer.StartDraw()
		self.frameCount += 1

	def _create_game_field(self):
		self.world.gravity = (0.0, 0.0)
		self.border = BoxBorder(self.world, self.gameSize, 1)
		# sets scale of renderer. this has no effect on rendering, only on mouse coordinate calculation
		self.renderer.setZoom((self.gameSize + 4 * self.border.thickness) / 2)
		self.renderer.setCenter(b2Vec2(self.gameSize / 2, self.gameSize / 2))

	def Keyboard(self, key):
		if key == 32:
			for ship in self.contactHandler.spaceships:
				heading = b2Vec2(math.cos(ship.body.angle), math.sin(ship.body.angle)) * 30
				rocket = BoxRocket(self.world, ship, heading)
				self.contactHandler.add_rocket(rocket)
