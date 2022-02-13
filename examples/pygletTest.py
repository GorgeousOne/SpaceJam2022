import pyglet


class SpaceWindow(pyglet.window.Window):

	def __init__(self):
		super(SpaceWindow, self).__init__(config=pyglet.gl.Config(sample_buffers=1, samples=8))
		self.set_size(800, 800)
		self.set_caption("Space Jam")
		self.batch = pyglet.graphics.Batch()

		self.batch.add_indexed(
			4, pyglet.gl.GL_TRIANGLES, None,
			[0, 1, 2, 0, 2, 3],
			('v2f', (
				200, 200,
				200, 300,
				300, 300,
				300, 200
			)),
			('c4f', (
				1.0, 1.0, 1.0, 0.2,
				1.0, 1.0, 1.0, 0.2,
				1.0, 1.0, 1.0, 0.0,
				1.0, 1.0, 1.0, 0.0
			))
		)

	def on_draw(self):
		self.clear()
		pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
		pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
		self.batch.draw()

if __name__ == '__main__':
	window = SpaceWindow()
	pyglet.app.run()
