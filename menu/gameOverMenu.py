import glooey
from pyglet import gl

from menu.gameMenu import GameMenu
from menu.menuWidget import Title, CustomButton, MenuLabel
from render.pygletWindow import PygletWindow


class GameOverGameMenu(GameMenu):

	def __init__(self, window: PygletWindow, return_callback):
		self.returnCallback = return_callback
		super().__init__(window)

	def _setup_gui(self):
		super()._setup_gui()

		container = glooey.VBox()
		container.set_default_cell_size(1)
		container.set_cell_padding(40)
		container.set_bottom_padding(50)
		container.set_alignment("center")

		self.resultTitle = Title("", font_size=24)
		container.add(self.resultTitle)

		self.timeText = MenuLabel("", font_size=15)
		self.timeText.set_alignment("center")
		container.add(self.timeText)

		return_btn = CustomButton("Return", lambda widget: self.returnCallback())
		return_btn.set_size_hint(200, 0)
		return_btn.set_alignment("center")
		return_btn.get_foreground().set_alignment("center")
		container.add(return_btn)

		self.root.add(container)
		self.hide()

	def set_time(self, ticks):
		self.timeText.set_text(str(ticks) + " rounds")

	def set_winner(self, winner: str):
		self.resultTitle.set_text(winner + " won!")

	def set_tie(self):
		self.resultTitle.set_text("It's a tie...")

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
