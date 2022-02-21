import pyglet

from game.boxBackground import BoxBackground
from game.gameMenu import GameMenu
from game.gameSimulation import GameSimulation
from gui.settings import fwSettings

from pyglet import gl

class SpaceJam:

	def get_game_projection(self):
		border_thickness = 2
		scale = self.windowSize / (self.gameSize + 2 * border_thickness)

		gl.glPushMatrix()
		gl.glScalef(scale, scale, 1)
		gl.glTranslatef(border_thickness, border_thickness, 0)

		matrix = (gl.GLfloat * 16)()
		gl.glGetFloatv(pyglet.gl.GL_MODELVIEW_MATRIX, matrix)
		gl.glPopMatrix()
		return matrix

	def __init__(self):
		self.windowSize = 600
		self.window = pyglet.window.Window(config=pyglet.gl.Config(sample_buffers=1, samples=8), width=self.windowSize, height=self.windowSize)
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
		self.simulation.reload()
		self.simulation.set_frame_count(self.menu.frameCount)
		self.simulation.add_pilots(self.menu.get_selected_pilot_classes())
		self.simulation.run()
		pass

if __name__ == '__main__':
	SpaceJam()
