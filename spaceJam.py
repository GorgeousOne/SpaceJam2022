import os

import pyglet

from game.boxBackground import BoxBackground
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

		icon_path = fileLoad.resource_path("res" + os.path.sep + "rocket-icon.png")
		self.window.set_icon(pyglet.image.load(icon_path))

		self.gameSize = 100

		# https://jotson.itch.io/gravity-pixel-font
		self.load_font("GravityRobotBold8.ttf")
		self.load_font("GravityRegular5.ttf")

		self.background = BoxBackground(self.gameSize, fwSettings.hz)
		self.menu = None
		self.game = None
		gl.glLoadMatrixf(self.get_game_projection())
		gl.glEnable(gl.GL_BLEND)
		gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

		self.game = GameSimulation(self.window)
		self.game.run()
		pyglet.app.run()

	def load_font(self, file_name: str):
		font_path = fileLoad.resource_path("res" + os.path.sep + file_name)
		pyglet.font.add_file(font_path)

if __name__ == '__main__':
	SpaceJam()
