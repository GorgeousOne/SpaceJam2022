import pyglet
from Box2D import b2Vec2
from pyglet import gl

from game.boxBackground import BoxBackground
from game.gameMenu import GameMenu
from gui.pygletDraw import PygletDraw
from gui.pygletWindow import PygletWindow


class SpaceJam2:

	def __init__(self):
		self.window = PygletWindow(None)
		self.windowSize = 600
		self.window.set_size(self.windowSize, self.windowSize)
		self.window.set_caption("Space Jam")

		self.gameSize = 100
		self.setup()

		background = BoxBackground(self.gameSize)
		renderer = PygletDraw()
		menu = GameMenu(self.window, renderer, background)

		menu.run()
		pyglet.app.run()
		pass

	def setup(self):
		gl.glViewport(0, 0, self.window.width, self.window.height)
		gl.glMatrixMode(gl.GL_PROJECTION)
		gl.glLoadIdentity()

		ratio = float(self.window.width) / self.window.height

		extents = b2Vec2(ratio * 25.0, 25.0)
		extents *= (self.gameSize + 4) / 50

		lower = b2Vec2(50, 50) - extents
		upper = b2Vec2(50, 50) + extents

		# L/R/B/T
		gl.gluOrtho2D(lower.x, upper.x, lower.y, upper.y)

		gl.glMatrixMode(gl.GL_MODELVIEW)
		gl.glLoadIdentity()
if __name__ == '__main__':
	SpaceJam2()
