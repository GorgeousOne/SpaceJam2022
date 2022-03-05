import glooey

from menu.gameMenu import GameMenu
from menu.menuWidget import Title, CustomButton
from render.pygletWindow import PygletWindow


class PauseGameMenu(GameMenu):

	def __init__(self, window: PygletWindow, continue_callback, return_callback):
		self.continueCallback = continue_callback
		self.returnCallback = return_callback
		super().__init__(window)

	def _setup_gui(self):
		super()._setup_gui()

		container = glooey.VBox()
		container.set_default_cell_size(1)
		container.set_cell_padding(40)
		container.set_bottom_padding(60)
		container.set_alignment("center")

		self.resultTitle = Title("", font_size=24)
		container.add(self.resultTitle)

		continue_btn = CustomButton("Continue", lambda widget: self.continueCallback())
		return_btn = CustomButton("Return", lambda widget: self.returnCallback())
		continue_btn.set_size_hint(200, 0)
		return_btn.set_size_hint(200, 0)
		continue_btn.set_alignment("center")
		return_btn.set_alignment("center")
		continue_btn.get_foreground().set_alignment("center")
		return_btn.get_foreground().set_alignment("center")

		container.add(continue_btn)
		container.add(return_btn)
		self.root.add(container)
