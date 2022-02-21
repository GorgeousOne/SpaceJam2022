import math
from typing import List

import pyglet
from Box2D import b2Vec2
from pyglet import gl

from game.boxBackground import BoxBackground
from game.boxBorder import BoxBorder
from game.boxContactListener import BoxContactListener
from game.boxRocket import BoxRocket
from game.gameHandler import GameHandler
from gui.pygletFramework import PygletFramework


class GameSimulation(PygletFramework):
	name = "Space Jam"

	def __init__(self, window: pyglet.window.Window, game_matrixf, background: BoxBackground):
		super(GameSimulation, self).__init__(window)

		self.gameMatrixF = game_matrixf
		self.background = background
		self.gameSize = 100
		self.frameCount = 0

		self.contactHandler = BoxContactListener(self.world)
		self.world.contactListener = self.contactHandler

		self.gameHandler = GameHandler(self.world, self.contactHandler, self.gameSize)
		# spaceship svg model currently has size 5
		self.spaceshipSize = 5
		# self.pilotHandler = PilotHandler(self.gameHandler, self.gameSize, 5)

		self._create_game_field()
		# self.pilotHandler.add_cmd_line_pilots()

	def set_frame_count(self, frame_count: int):
		self.frameCount = frame_count

	def reload(self):
		self.gameHandler.reset()
		self.contactHandler.reset()

	def add_pilots(self, pilot_classes: List):
		for pilot in pilot_classes:
			self.gameHandler.spawn_spaceship(pilot(self.gameSize, self.spaceshipSize))

	def Redraw(self):
		gl.glPushMatrix()
		gl.glLoadMatrixf(self.gameMatrixF)

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
		gl.glPopMatrix()

		self.frameCount += 1

	def _create_game_field(self):
		self.world.gravity = (0.0, 0.0)
		self.border = BoxBorder(self.world, self.gameSize, 1)

		# sets scale of renderer. this has no effect on rendering, only on mouse coordinate calculation
		self.renderer.setZoom((self.gameSize + self.border.thickness) / 50)
		self.renderer.setCenter(b2Vec2(self.gameSize / 2, self.gameSize / 2))

	def Keyboard(self, key):
		if key == 32:
			for ship in self.contactHandler.spaceships:
				heading = b2Vec2(math.cos(ship.body.angle), math.sin(ship.body.angle)) * 30
				rocket = BoxRocket(self.world, ship, heading)
				self.contactHandler.add_rocket(rocket)
