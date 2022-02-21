import pyglet

from game.boxBackground import BoxBackground
from game.gameMenu import GameMenu
from gameSimulation import GameSimulation
from gui.pygletDraw import PygletDraw
from gui.settings import fwSettings

from pyglet import gl

class SpaceJam2:

	def get_game_projection(self):
		border_thickness = 2
		scale = self.windowSize / (self.gameSize + 2 * border_thickness)

		gl.glPushMatrix()
		gl.glScalef(scale, scale, 1)
		gl.glTranslatef(border_thickness, border_thickness, 0)

		matrix = (gl.GLfloat * 16)()
		gl.glGetFloatv(pyglet.gl.GL_MODELVIEW_MATRIX, matrix)
		gl.glPopMatrix()
		print(type(matrix))
		return matrix

	def __init__(self):
		self.window = pyglet.window.Window(config=pyglet.gl.Config(sample_buffers=1, samples=8))
		self.windowSize = 600
		self.window.set_size(self.windowSize, self.windowSize)

		self.window.set_caption("Space Jam")
		self.gameSize = 100

		self.background = BoxBackground(self.gameSize, fwSettings.hz)
		projection_matrix = self.get_game_projection()
		self.menu = GameMenu(self.window, projection_matrix, self.background, self._start_game)
		self.simulation = GameSimulation(self.window, projection_matrix, self.background)

		self.menu.run()
		pyglet.app.run()
		pass

	def _start_game(self):
		self.menu.cancel()
		self.simulation.set_frame_count(self.menu.frameCount)
		self.simulation.run()
		pass

if __name__ == '__main__':
	SpaceJam2()
