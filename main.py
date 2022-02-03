import pyglet


class SpaceWindow(pyglet.window.Window):

	def __init__(self):
		super(SpaceWindow, self).__init__(config=pyglet.gl.Config(sample_buffers=1, samples=8))
		self.set_size(800, 800)
		self.set_caption("Space Jam")
		self.batch = pyglet.graphics.Batch()
		# self.set_fps_limit(60)

	def on_draw(self):
		self.clear()

		pyglet.graphics.draw_indexed(
			3,
			pyglet.gl.GL_TRIANGLES,
			[0, 1, 2],
			("v2i", (300, 350,
			         250, 250,
			         350, 250))
		)

	def create_border(self, width, height, thickness):
		size = self.get_size()

		pass
		

if __name__ == '__main__':
	window = SpaceWindow()
	pyglet.app.run()
