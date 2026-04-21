from __future__ import annotations

import math

from geoengine.algebra.matrix import Matrix3x3
from geoengine.algebra.vector import Vector3D
from geoengine.scenes import build_demo_world


def build_portfolio_report() -> str:
    matrix = Matrix3x3.from_euler(math.radians(25), math.radians(30), math.radians(15)) * Matrix3x3.shear_xy(0.2, 0.08)
    transformed_vector = matrix * Vector3D(1.0, 1.0, 0.5)

    world = build_demo_world()
    for _ in range(120):
        world.step(1 / 120)
    snapshot = world.snapshot()

    lines = [
        "GeoEngine report",
        "---------------",
        f"det(M) = {matrix.determinant():.4f}",
        f"M * v = ({transformed_vector.x:.3f}, {transformed_vector.y:.3f}, {transformed_vector.z:.3f})",
        f"particles = {snapshot.particle_count}",
        f"kinetic_energy = {snapshot.total_energy:.4f}",
        (
            "momentum = "
            f"({snapshot.total_momentum.x:.4f}, {snapshot.total_momentum.y:.4f}, {snapshot.total_momentum.z:.4f})"
        ),
    ]
    return "\n".join(lines)
