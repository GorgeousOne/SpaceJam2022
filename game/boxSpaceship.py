import math
from typing import List

import numpy as np
from Box2D import (b2World, b2PolygonShape, b2FixtureDef, b2Color, b2Vec2)

from render.pygletDraw import PygletDraw
from logic.location import Location
from logic.pilotAction import PilotAction
from logic.spaceshipPilot import SpaceshipPilot

hitbox = [
	(-1.37, -0.58),
	(-1.89, -0.43),
	(-1.89, 0.43),
	(-1.37, 0.58),
	(0.31, 1.00),
	(1.54, 0.91),
	(2.45, 0.59),
	(3.11, 0.00),
	(2.45, -0.59),
	(1.54, -0.91),
	(0.31, -1.00)
]

viewbox = [
	(0.00, 0.00),
	(0.13, -0.31),
	(0.44, -0.44),
	(0.31, -1.00),
	(-0.33, -1.42),
	(-1.11, -1.52),
	(-1.74, -1.39),
	(-1.50, -0.95),
	(-1.29, -0.87),
	(-1.37, -0.58),
	(-1.89, -0.43),
	(-1.89, 0.43),
	(-1.37, 0.58),
	(-1.29, 0.87),
	(-1.50, 0.95),
	(-1.74, 1.39),
	(-1.11, 1.52),
	(-0.33, 1.42),
	(0.31, 1.00),
	(1.54, 0.91),
	(2.45, 0.59),
	(3.11, 0.00),
	(2.45, -0.59),
	(1.54, -0.91),
	(0.31, -1.00),
	(0.44, -0.44),
	(0.75, -0.31),
	(0.88, 0.00),
	(0.75, 0.31),
	(0.44, 0.44),
	(0.13, 0.31)
]

import tripy
viewbox_triangles = tripy.earclip(viewbox)
triangle_indices = [viewbox.index(v) for t in viewbox_triangles for v in t]
viewbox = [b2Vec2(v[0], v[1]) for v in viewbox]

class BoxSpaceship:

	def __init__(self, world: b2World, pilot: SpaceshipPilot, health: int, color: b2Color = b2Color(1., 1., 1.), pos: b2Vec2 = b2Vec2(0, 0), angle: float = 0):
		self.pilot = pilot
		self.max_health = health
		self.health = health
		self.energy = 0

		self.color = b2Color(color)
		self.shape = b2PolygonShape(vertices=hitbox)
		self.body = world.CreateDynamicBody(
			userData=self,  # adds a reference on the body to the spaceship object
			position=b2Vec2(pos),
			angle=angle,
			linearDamping=0,
			shapes=[self.shape],
			shapeFixture=b2FixtureDef(
				restitution=0.2,  # bounciness between 0 and 1
			),
			fixedRotation=True  # fixes angular velocity to one value
		)

	def update(self, new_energy) -> PilotAction:
		self.energy = new_energy
		return self.pilot.update(self.get_location(), self.health, self.energy)

	def process_scan(self, current_action: PilotAction, located_rockets: List[Location]) -> PilotAction:
		return self.pilot.process_scan(current_action, located_rockets)

	def move(self, impulse: b2Vec2):
		self.body.linearVelocity += impulse
		if self.body.linearVelocity.y != 0 or self.body.linearVelocity.x != 0:
			self.body.angle = math.atan2(self.body.linearVelocity.y, self.body.linearVelocity.x)

	def damage(self, amount: int):
		self.health -= amount
		if self.health <= 0:
			self.color = b2Color(255, 0, 0)

	def get_location(self):
		pos = self.body.position
		vel = self.body.linearVelocity
		return Location(np.array([pos.x, pos.y]), np.array([vel.x, vel.y]))

	def display(self, renderer: PygletDraw, layer_index: int, text_layer_index: int):
		vertices = []

		for v in viewbox:
			vertices.append(self.body.GetWorldPoint(v))
		renderer.DrawIndexedTriangles(layer_index, vertices, triangle_indices, self.color)

		pos = b2Vec2(self.body.position) + b2Vec2(0, 7)
		renderer.DrawText(text_layer_index, type(self.pilot).__name__, pos, "GravityRegular5", 8)

		damaged_color = b2Color(1, 1, 1)
		damaged_color.a = 0.2
		self.display_healthbar(renderer, b2Color(1, 1, 1), damaged_color)

	def display_healthbar(self, renderer: PygletDraw, healthy_color, damaged_color):
		width = 10
		height = 0.6
		border = (float(self.health) / self.max_health - 0.5) * width
		offset = 4

		pos = b2Vec2(self.body.position)
		healthy_verts = [
			b2Vec2(pos) + b2Vec2(-width/2, offset + height),
			b2Vec2(pos) + b2Vec2(border, offset + height),
			b2Vec2(pos) + b2Vec2(border, offset),
			b2Vec2(pos) + b2Vec2(-width/2, offset),
		]
		damaged_verts = [
			b2Vec2(pos) + b2Vec2(border, offset + height),
			b2Vec2(pos) + b2Vec2(width / 2, offset + height),
			b2Vec2(pos) + b2Vec2(width / 2, offset),
			b2Vec2(pos) + b2Vec2(border, offset),
		]
		renderer.DrawGradientRect(7, healthy_verts, healthy_color, healthy_color)
		renderer.DrawGradientRect(7, damaged_verts, damaged_color, damaged_color)