import math

from geoengine.algebra.vector import Vector3D
from geoengine.physics.particle import Particle
from geoengine.physics.world import World


def test_particles_exchange_impulse_after_collision():
    world = World(gravity=Vector3D.zero(), floor_y=-10.0, bounds_x=(-10.0, 10.0))
    first = Particle(position=Vector3D(-0.4, 0.0, 0.0), velocity=Vector3D(1.0, 0.0, 0.0), mass=1.0, radius=0.5)
    second = Particle(position=Vector3D(0.4, 0.0, 0.0), velocity=Vector3D(-1.0, 0.0, 0.0), mass=1.0, radius=0.5)
    world.add_particle(first)
    world.add_particle(second)

    world.resolve_collisions()

    assert math.isclose(first.velocity.x, -0.92, abs_tol=1e-9)
    assert math.isclose(second.velocity.x, 0.92, abs_tol=1e-9)


def test_gravity_changes_vertical_velocity():
    world = World(gravity=Vector3D(0.0, -9.81, 0.0), floor_y=-10.0, bounds_x=(-10.0, 10.0))
    particle = Particle(position=Vector3D(0.0, 5.0, 0.0), velocity=Vector3D.zero())
    world.add_particle(particle)

    world.step(0.5)

    assert particle.velocity.y < 0
