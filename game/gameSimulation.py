from typing import List

import pyglet
from Box2D import b2Vec2
from pyglet.window import key

from game.boxBackground import BoxBackground
from game.boxBorder import BoxBorder
from game.boxContactListener import BoxContactListener
from game.gameHandler import GameHandler
from menu.gameOverMenu import GameOverGameMenu
from menu.gameMenu import GameMenu
from menu.pauseMenu import PauseGameMenu
from menu.startMenu import StartGameMenu
from render.pygletFramework import PygletFramework


class GameSimulation(PygletFramework):

	def __init__(self, window: pyglet.window.Window):
		super(GameSimulation, self).__init__(window)
		self.gameSize = 100
		self.spaceshipSize = 5  # spaceship svg model currently has size 5

		self.background = BoxBackground(self.gameSize, self.settings.hz)
		self.gui = None

		self.arePhysicsOn = False
		self.isGameOver = True
		self.isGamePaused = False
		self.doDisplayNames = True

		self.frameCount = 0
		self.gameTicksPerSecond = 5

		self.contactHandler = BoxContactListener(self.world)
		self.world.contactListener = self.contactHandler
		self.gameHandler = GameHandler(self.world, self.contactHandler, self.gameSize, self.gameTicksPerSecond)
		self._create_game_field()

		self.startMenu = StartGameMenu(self.window, lambda: self.start_simulation(self.startMenu.get_selected_pilot_classes()))
		self.gamOverMenu = GameOverGameMenu(self.window, self._return_to_start)
		self.pauseMenu = PauseGameMenu(self.window, self.continue_game, self._return_to_start)
		self._return_to_start()

	def _show_gui(self, gui: GameMenu):
		self._hide_gui()
		self.gui = gui
		self.gui.unhide()

	def _hide_gui(self):
		if self.gui:
			self.gui.hide()
			self.gui = None

	def _return_to_start(self):
		self.arePhysicsOn = False
		self.isGameOver = True
		self.isGamePaused = False
		self.contactHandler.reset()
		self._show_gui(self.startMenu)

	def start_simulation(self, pilot_classes: List):
		self._hide_gui()
		for pilot in pilot_classes:
			self.gameHandler.spawn_spaceship(pilot(self.gameSize, self.spaceshipSize))

		self.stepCount = 0
		self.arePhysicsOn = True
		self.isGameOver = False

	def pause_game(self):
		self.isGamePaused = True
		self._show_gui(self.pauseMenu)

	def continue_game(self):
		if not self.isGamePaused:
			return
		self.isGamePaused = False
		self._hide_gui()

	def _announce_result(self):
		self.isGameOver = True
		self._show_gui(self.gamOverMenu)

		if len(self.contactHandler.spaceships) > 0:
			self.gamOverMenu.set_winner(next(iter(self.contactHandler.spaceships)).name)
		else:
			self.gamOverMenu.set_tie()

	def display(self, dt):
		if self.arePhysicsOn:
			self.SimulationLoop(1 / self.settings.hz)

		# don't draw shapes and texts on same layer :P
		self.window.clear()
		self.renderer.clear_batch()
		self.background.display(self.renderer, 0, self.frameCount)

		for explosion in self.contactHandler.explosions:
			explosion.display(self.renderer, 1)
		for scan in self.contactHandler.scans:
			scan.display(self.renderer, 1)
		for rocket in self.contactHandler.rockets:
			rocket.display(self.renderer, 1)

		text_layer = 4
		for ship in self.contactHandler.spaceships:
			ship.display(self.renderer, 2, text_layer if self.doDisplayNames else None)
			text_layer += 1

		self.border.display(self.renderer, 3)
		self.renderer.StartDraw()

		if self.gui:
			self.gui.display()
		self.frameCount += 1

	def Step(self):
		if self.isGamePaused:
			return
		super().Step()

		if self.isGameOver:
			return
		if len(self.contactHandler.spaceships) < 2:
			self._announce_result()
			return
		if self.stepCount % (self.settings.hz // 5) == 0:
			self.gameHandler.update()
		self.contactHandler.remove_bodies()

	def _create_game_field(self):
		self.world.gravity = (0.0, 0.0)
		self.border = BoxBorder(self.world, self.gameSize, 1)
		# sets scale of renderer. this has no effect on rendering, only on mouse coordinate calculation
		self.renderer.setZoom((self.gameSize + 4 * self.border.thickness) / 2)
		self.renderer.setCenter(b2Vec2(self.gameSize / 2, self.gameSize / 2))

	def Keyboard(self, pressed):
		if pressed == key.BACKSPACE:
			self._return_to_start()
		elif pressed == key.SPACE:
			if self.isGameOver:
				self._return_to_start()
			elif self.arePhysicsOn:
				if self.isGamePaused:
					self.continue_game()
				else:
					self.pause_game()
		elif pressed == key.F1:
			self.doDisplayNames = not self.doDisplayNames
