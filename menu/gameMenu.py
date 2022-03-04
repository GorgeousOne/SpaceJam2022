from pyglet import gl

from menu.menuWidget import MenuGui
from render.pygletWindow import PygletWindow


class GameMenu:

	def __init__(self, window: PygletWindow):
		self.window = window
		self._setup_gui()
		self.hide()

	def _setup_gui(self):
		self.root = MenuGui(self.window)

	def unhide(self):
		self.window.push_handlers(self.root)
		self.root.unhide()

	def hide(self):
		self.root.hide()
		self.window.remove_handlers(self.root)

	def display(self):
		gl.glPushMatrix()
		gl.glLoadIdentity()
		self.root.display()
		gl.glPopMatrix()
