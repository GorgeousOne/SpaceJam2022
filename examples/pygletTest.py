import glooey
import pyglet


class MyLabel(glooey.Label):
	custom_font_name = "Segoe UI"
	custom_color = '#babdb6'
	custom_font_size = 10
	# custom_alignment = 'center'


class MyTitle(glooey.Label):
	custom_color = '#eeeeec'
	custom_font_size = 12
	custom_alignment = 'center'
	custom_bold = True


class MenuButton(glooey.Button):
	Foreground = MyLabel
	custom_alignment = 'fill'

	class Base(glooey.Background):
		custom_color = '#204a87'

	class Over(glooey.Background):
		custom_color = '#3465a4'

	class Down(glooey.Background):
		custom_color = '#729fcff'

	def __init__(self, text, response):
		super().__init__(text)
		self.response = response

	def on_click(self, widget):
		print(self.response)


window = pyglet.window.Window()
gui = glooey.Gui(window, clear_before_draw=False)

root = glooey.VBox()
root.alignment = 'center'

buttons = [
	MenuButton("🤖 Afk Boteé", "Cool"),
	MenuButton("Circle Bot", "Aha"),
	MenuButton("I don't know that!", "Mhh"),
]

pilot_table = glooey.Grid(num_cols=2, num_rows=len(buttons) + 1)
root.add(pilot_table)

title_available = MyTitle("Available Pilots")
title_selected = MyTitle("Selected Pilots")
pilot_table[0, 0] = title_available
pilot_table[0, 1] = title_selected

for i in range(len(buttons)):
	pilot_table[i + 1, 0] = buttons[i]

gui.add(root)
pyglet.app.run()
