from __future__ import annotations

from geoengine.algebra.vector import Vector3D
from geoengine.physics.particle import Particle
from geoengine.physics.world import World


CUBE_VERTICES = [
    Vector3D(-1.0, -1.0, -1.0),
    Vector3D(1.0, -1.0, -1.0),
    Vector3D(1.0, 1.0, -1.0),
    Vector3D(-1.0, 1.0, -1.0),
    Vector3D(-1.0, -1.0, 1.0),
    Vector3D(1.0, -1.0, 1.0),
    Vector3D(1.0, 1.0, 1.0),
    Vector3D(-1.0, 1.0, 1.0),
]

CUBE_EDGES = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7),
]


def build_demo_world() -> World:
    world = World(gravity=Vector3D(0.0, -9.6, 0.0), floor_y=-2.8, bounds_x=(-4.5, 4.5))
    world.add_particle(
        Particle(
            position=Vector3D(-2.4, 1.8, 0.0),
            velocity=Vector3D(2.8, 0.6, 0.0),
            mass=1.0,
            radius=0.35,
            restitution=0.92,
            color="#fb7185",
        )
    )
    world.add_particle(
        Particle(
            position=Vector3D(1.2, 0.8, 0.0),
            velocity=Vector3D(-1.8, -0.3, 0.0),
            mass=1.8,
            radius=0.48,
            restitution=0.88,
            color="#38bdf8",
        )
    )
    world.add_particle(
        Particle(
            position=Vector3D(0.0, 2.7, 0.0),
            velocity=Vector3D(0.7, -1.2, 0.0),
            mass=0.7,
            radius=0.30,
            restitution=0.94,
            color="#facc15",
        )
    )
    return world
