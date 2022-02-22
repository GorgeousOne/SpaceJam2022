import os

import pyglet

from game.boxBackground import BoxBackground
from game.gameMenu import GameMenu
from game.gameSimulation import GameSimulation
from render.settings import fwSettings

from pyglet import gl

from util import fileLoad


class SpaceJam:

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

	def __init__(self):
		self.windowSize = 600
		self.window = pyglet.window.Window(config=pyglet.gl.Config(sample_buffers=1, samples=8), width=self.windowSize, height=self.windowSize)
		self.window.set_caption("Space Jam")
		self.gameSize = 100

		# https://jotson.itch.io/gravity-pixel-font
		font_path = fileLoad.resource_path(os.path.sep.join(["res", "GravityBold8.ttf"]))
		pyglet.font.add_file(font_path)

		self.background = BoxBackground(self.gameSize, fwSettings.hz)
		self.menu = None
		self.simulation = None
		gl.glLoadMatrixf(self.get_game_projection())

		self._start_menu()
		pyglet.app.run()

	def _start_menu(self):
		self.menu = GameMenu(self.window, self.background, self._start_game)
		if self.simulation:
			self.simulation.cancel()
			self.menu.set_frame_count(self.simulation.frameCount)
			self.simulation = None
		self.menu.run(fwSettings.hz)

	def _start_game(self):
		self.simulation = GameSimulation(self.window, self.background, self.menu.get_selected_pilot_classes(), self._start_menu)
		if self.menu:
			self.menu.cancel()
			self.simulation.set_frame_count(self.menu.frameCount)
			self.menu = None
		self.simulation.run()

if __name__ == '__main__':
	SpaceJam()
