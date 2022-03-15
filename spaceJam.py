import os
import traceback
from typing import List

import pyglet
from Box2D import b2Vec2
from pyglet import gl
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
from util import fileLoad


class SpaceJam(PygletFramework):

	def __init__(self, window_size: int):
		super(SpaceJam, self).__init__(pyglet.window.Window(config=pyglet.gl.Config(sample_buffers=1, samples=8), width=window_size, height=window_size))
		self.windowSize = window_size
		self.window.set_caption("Space Jam")
		icon_path = fileLoad.resource_path("res" + os.path.sep + "rocket.png")
		self.window.set_icon(pyglet.image.load(icon_path))

		# https://jotson.itch.io/gravity-pixel-font
		fileLoad.load_font("GravityRobotBold8.ttf")
		fileLoad.load_font("GravityRegular5.ttf")

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

		gl.glLoadMatrixf(self.get_game_projection())
		gl.glEnable(gl.GL_BLEND)
		gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

		self._return_to_start()

	def get_game_projection(self):
		border_thickness = 1
		scale = self.windowSize / (self.gameSize + 4 * border_thickness)

		gl.glPushMatrix()
		gl.glLoadIdentity()
		gl.glMatrixMode(gl.GL_MODELVIEW)
		gl.glScalef(scale, scale, 1)
		gl.glTranslatef(2 * border_thickness, 2 * border_thickness, 0)

		matrix = (gl.GLfloat * 16)()
		gl.glGetFloatv(pyglet.gl.GL_MODELVIEW_MATRIX, matrix)
		gl.glPopMatrix()
		return matrix

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
		self.gameHandler.reset()

		for pilot in pilot_classes:
			try:
				instance = pilot()
				self.gameHandler.spawn_spaceship(instance)
			except Exception as e:
				print("Could not create spaceship \"" + pilot.__name__ + "\":")
				print(traceback.format_exc())

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
		if self.stepCount % (self.settings.hz // self.gameTicksPerSecond) == 0:
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


if __name__ == '__main__':
	SpaceJam(600).run()
	pyglet.app.run()