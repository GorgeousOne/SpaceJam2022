import math
from typing import List

import numpy as np
from Box2D import (b2World, b2PolygonShape, b2FixtureDef, b2Color, b2Vec2)

from render.pygletDraw import PygletDraw
from logic.location import Location
from logic.pilotAction import PilotAction, ScanAction
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

	def __init__(self, world: b2World, pilot: SpaceshipPilot, max_health: int, max_energy: float, color: b2Color = b2Color(1., 1., 1.), pos: b2Vec2 = b2Vec2(0, 0), angle: float = 0):
		self.pilot = pilot
		self.name = type(pilot).__name__
		self.displayName = self.name[0:16] if len(self.name) > 16 else self.name

		self.max_health = max_health
		self.health = max_health
		self.max_energy = max_energy
		self.energy = max_energy

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

	def add_energy(self, energy_amount: int):
		self.energy = min(self.max_energy, self.energy + energy_amount)

	def use_energy(self, energy_amount: float):
		self.energy = max(0, self.energy - energy_amount)

	def prepare_scan(self, game_tick: int, ticks_per_second: int) -> ScanAction:
		return self.pilot.prepare_scan(game_tick, self.get_location(ticks_per_second), self.health, self.energy)

	def update(self, game_tick: int, ticks_per_second: int, located_rockets: List[np.ndarray]) -> PilotAction:
		return self.pilot.update(game_tick, self.get_location(ticks_per_second), self.health, self.energy, located_rockets)

	def move(self, acceleration: b2Vec2, max_velocity_per_tick, ticks_per_second):
		self.body.linearVelocity += acceleration * ticks_per_second
		current_velocity = self.body.linearVelocity.length

		max_velocity = max_velocity_per_tick * ticks_per_second
		if current_velocity > max_velocity:
			self.body.linearVelocity *= max_velocity / current_velocity

		if self.body.linearVelocity.y != 0 or self.body.linearVelocity.x != 0:
			self.body.angle = math.atan2(self.body.linearVelocity.y, self.body.linearVelocity.x)

	def damage(self, amount: int):
		self.health = max(0, self.health - amount)

	def get_location(self, ticks_per_second:int = 1):
		pos = self.body.position
		vel = self.body.linearVelocity / ticks_per_second
		return Location(np.array([pos.x, pos.y]), np.array([vel.x, vel.y]))

	def display(self, renderer: PygletDraw, layer_index: int, text_layer_index: int):
		vertices = []

		for v in viewbox:
			vertices.append(self.body.GetWorldPoint(v))
		renderer.DrawIndexedTriangles(layer_index, vertices, triangle_indices, self.color)
		pos = b2Vec2(self.body.position) + b2Vec2(0, 7)

		if text_layer_index:
			renderer.DrawText(text_layer_index, self.displayName, pos, "GravityRegular5", 8)
		self.display_bar(renderer, layer_index, self.health/self.max_health, 5.0, b2Color(0.9, 0.0, 0.0))
		self.display_bar(renderer, layer_index, self.energy/self.max_energy, 4.0, b2Color(0.1, 0.25, 1.0))

	def display_bar(self, renderer: PygletDraw, layer_index: int, percent: float, offset: float, color: b2Color = b2Color(1.0, 1.0, 1.0), width: float = 10, height: float = 0.6):
		color_missing = b2Color(color)
		color_missing.a = 0.5

		pos = self.body.position
		x_min = pos.x - width/2
		x_max = x_min + width
		x_mid = x_min + percent * width

		y_min = pos.y + offset
		y_max = y_min + height

		if percent > 0:
			remaining_verts = [
				b2Vec2(x_min, y_min),
				b2Vec2(x_min, y_max),
				b2Vec2(x_mid, y_max),
				b2Vec2(x_mid, y_min),
			]
			renderer.DrawGradientRect(layer_index, remaining_verts, color, color)
		if percent < 1:
			missing_verts = [
				b2Vec2(x_mid, y_min),
				b2Vec2(x_mid, y_max),
				b2Vec2(x_max, y_max),
				b2Vec2(x_max, y_min),
			]
			renderer.DrawGradientRect(layer_index, missing_verts, color_missing, color_missing)
