import pyglet
from Box2D import b2Vec2
from pyglet import gl

from game.boxBackground import BoxBackground
from game.gameMenu import GameMenu
from gui.pygletDraw import PygletDraw
from gui.settings import fwSettings


class SpaceJam2:

	def __init__(self):
		self.window = pyglet.window.Window(config=pyglet.gl.Config(sample_buffers=1, samples=8))
		self.windowSize = 600
		self.window.set_size(self.windowSize, self.windowSize)
		self.window.set_caption("Space Jam")
		self.gameSize = 100

		self.background = BoxBackground(self.gameSize, fwSettings.hz)
		self.renderer = PygletDraw(self.window)
		menu = GameMenu(self.window, self.renderer, self.gameSize, self.background)

		menu.run()
		pyglet.app.run()
		pass

if __name__ == '__main__':
	SpaceJam2()
