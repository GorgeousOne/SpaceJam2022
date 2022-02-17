import pyglet
import glooey

# Define a custom style for text.  We'll inherit the ability to render text
# from the Label widget provided by glooey, and we'll define some class
# variables to customize the text style.

class MyLabel(glooey.Label):
    custom_color = '#babdb6'
    custom_font_size = 10
    custom_alignment = 'center'

# If we want another kind of text, for example a bigger font for section
# titles, we just have to derive another class:

class MyTitle(glooey.Label):
    custom_color = '#eeeeec'
    custom_font_size = 12
    custom_alignment = 'center'
    custom_bold = True

# It's also common to style a widget with existing widgets or with new
# widgets made just for that purpose.  The button widget is a good example.
# You can give it a Foreground subclass (like MyLabel from above) to tell it
# how to style text, and Background subclasses to tell it how to style the
# different mouse rollover states:

class MyButton(glooey.Button):
    Foreground = MyLabel
    custom_alignment = 'fill'

    # More often you'd specify images for the different rollover states, but
    # we're just using colors here so you won't have to download any files
    # if you want to run this code.

    class Base(glooey.Background):
        custom_color = '#204a87'

    class Over(glooey.Background):
        custom_color = '#3465a4'

    class Down(glooey.Background):
        custom_color = '#729fcff'

    # Beyond just setting class variables in our widget subclasses, we can
    # also implement new functionality.  Here we just print a programmed
    # response when the button is clicked.

    def __init__(self, text, response):
        super().__init__(text)
        self.response = response

    def on_click(self, widget):
        print(self.response)

# Use pyglet to create a window as usual.

window = pyglet.window.Window()

# Create a Gui object, which will manage the whole widget hierarchy and
# interact with pyglet to handle events.

gui = glooey.Gui(window)

# Create a VBox container, which will arrange any widgets we give it into a
# vertical column.  Center-align it, otherwise the column will take up the
# full height of the window and put too much space between our widgets.

vbox = glooey.VBox()
vbox.alignment = 'center'

# Create a widget to pose a question to the user using the "title" text
# style,  then add it to the top of the vbox.

title = MyTitle("What...is your favorite color?")
vbox.add(title)

# Create several buttons with different answers to the above question, then
# add each one to the vbox in turn.

buttons = [
       MyButton("Blue.", "Right, off you go."),
       MyButton("Blue. No yel--", "Auuuuuuuugh!"),
       MyButton("I don't know that!", "Auuuuuuuugh!"),
]
for button in buttons:
   vbox.add(button)

# Finally, add the vbox to the GUI.  It's always best to make this the last
# step, because once a widget is attached to the GUI, updating it or any of
# its children becomes much more expensive.

gui.add(vbox)

# Run pyglet's event loop as usual.

pyglet.app.run()