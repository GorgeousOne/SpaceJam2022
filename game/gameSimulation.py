import math
from typing import List

import pyglet
from Box2D import b2Vec2

from game.boxBackground import BoxBackground
from game.boxBorder import BoxBorder
from game.boxContactListener import BoxContactListener
from game.boxRocket import BoxRocket
from game.gameHandler import GameHandler
from menu.startMenu import StartMenu
from menu.gameOverMenu import GameOverMenu
from render.pygletFramework import PygletFramework


class GameSimulation(PygletFramework):
	name = "Space Jam"

	def __init__(self, window: pyglet.window.Window):
		super(GameSimulation, self).__init__(window)
		self.gameSize = 100
		self.spaceshipSize = 5  # spaceship svg model currently has size 5

		self.background = BoxBackground(self.gameSize, self.settings.hz)
		self.gui = None
		self.isSimulationRunning = False

		self.frameCount = 0

		self.contactHandler = BoxContactListener(self.world)
		self.world.contactListener = self.contactHandler
		self.gameHandler = GameHandler(self.world, self.contactHandler, self.gameSize)
		self._create_game_field()

		self.startMenu = StartMenu(self.window, lambda: self.start_simulation(self.startMenu.get_selected_pilot_classes()))
		self.gamOverMenu = GameOverMenu(self.window, self._return_to_start)
		self._return_to_start()

	def _return_to_start(self):
		self.contactHandler.reset()
		self.isSimulationRunning = False
		# remove any previous gui from window events
		if self.gui:
			self.gui.stop()

		self.gui = self.startMenu
		self.startMenu.start()

	def start_simulation(self, pilot_classes: List):
		if self.gui:
			self.gui.stop()
			self.gui = None

		for pilot in pilot_classes:
			self.gameHandler.spawn_spaceship(pilot(self.gameSize, self.spaceshipSize))
		self.isSimulationRunning = True
		self.stepCount = 0

	def pause_simulation(self):
		self.isSimulationRunning = False

	def display(self, dt):
		self.window.clear()

		if self.isSimulationRunning:
			self.SimulationLoop(1 / self.settings.hz)

		# don't draw shapes and texts on same layer :P
		self.background.display(self.renderer, 0, self.frameCount)

		# for explosion in self.contactHandler.explosions:
		# 	explosion.display(self.renderer, 1)
		for scan in self.contactHandler.scans:
			scan.display(self.renderer, 1)
		for rocket in self.contactHandler.rockets:
			rocket.display(self.renderer, 1)

		text_layer = 4
		for ship in self.contactHandler.spaceships:
			ship.display(self.renderer, 2, text_layer)
			text_layer += 1

		self.border.display(self.renderer, 3)
		self.renderer.StartDraw()

		if self.gui:
			self.gui.display()
		self.frameCount += 1
		self.window.invalid = True

	def Step(self):
		super().Step()
		if len(self.contactHandler.spaceships) < 2:
			self.announce_result()
			return

		if self.stepCount % (self.settings.hz // 5) == 0:
			self.gameHandler.update()
		self.contactHandler.remove_bodies()

	def announce_result(self):
		self.gui = self.gamOverMenu
		self.gamOverMenu.start()

		if len(self.contactHandler.spaceships) > 0:
			self.gamOverMenu.set_winner(next(iter(self.contactHandler.spaceships)).name)

	def _create_game_field(self):
		self.world.gravity = (0.0, 0.0)
		self.border = BoxBorder(self.world, self.gameSize, 1)
		# sets scale of renderer. this has no effect on rendering, only on mouse coordinate calculation
		self.renderer.setZoom((self.gameSize + 4 * self.border.thickness) / 2)
		self.renderer.setCenter(b2Vec2(self.gameSize / 2, self.gameSize / 2))

	# def Keyboard(self, key):
	# 	if key == 32:
	# 		for ship in self.contactHandler.spaceships:
	# 			heading = b2Vec2(math.cos(ship.body.angle), math.sin(ship.body.angle)) * 30
	# 			rocket = BoxRocket(self.world, ship, heading)
	# 			self.contactHandler.add_rocket(rocket)
