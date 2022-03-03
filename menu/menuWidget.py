import glooey
import pyglet


class MenuLabel(glooey.Label):
	custom_font_name = "GravityBold8"
	custom_color = '#DDDDDD'
	custom_font_size = 12
	custom_padding = 10

class Title(glooey.Label):
	custom_font_name = "GravityBold8"
	custom_font_size = 12
	custom_color = '#FFFFFF'
	custom_alignment = 'center'

class VScrollBox(glooey.ScrollBox):
	class VBar(glooey.VScrollBar):
		pass

class ScrollList(glooey.VBox):
	custom_alignment = 'top'
	custom_default_cell_size = 1
	custom_cell_padding = 15

	def __init__(self, name):
		super().__init__()
		self.header = Title(name)
		self.table = VScrollBox()

		self.table.set_height_hint(360)
		self.tableContents = glooey.VBox()
		self.tableContents.set_cell_padding(10)
		self.tableContents.set_default_cell_size(1)

		self.add(self.header)
		self.add(self.table)
		self.table.add(self.tableContents)

	def add_elem(self, elem: glooey.Widget):
		self.tableContents.add(elem)

	def remove_elem(self, elem: glooey.Widget):
		self.tableContents.remove(elem)

	def get_elems(self):
		return self.tableContents.get_children()


class CustomButton(glooey.Button):
	Foreground = MenuLabel
	custom_alignment = 'fill'

	class Base(glooey.Background):
		custom_color = '#1940ff'

	class Over(glooey.Background):
		custom_color = '#3859FF'

	class Down(glooey.Background):
		custom_color = '#5773FF'

	class Off(glooey.Background):
		custom_color = "#696969"

	def __init__(self, text: str, callback = None):
		super().__init__(text)
		self.callback = callback

	def on_click(self, widget):
		if self.callback:
			self.callback(self)


class MenuGui(glooey.Gui):

	def __init__(self, window: pyglet.window.Window):
		super().__init__(window, clear_before_draw=False)

	def display(self):
		super().on_draw()

	def on_draw(self):
		"""
		Disables auto drawing
		"""
		pass
