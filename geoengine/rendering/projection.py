from __future__ import annotations

from dataclasses import dataclass

from geoengine.algebra.vector import Vector3D


@dataclass(slots=True, frozen=True)
class Projector:
    width: int
    height: int
    camera_distance: float = 6.5
    focal_length: float = 240.0

    def project(self, point: Vector3D) -> tuple[float, float]:
        depth = self.camera_distance - point.z
        factor = self.focal_length / max(depth, 0.5)
        x = self.width / 2 + point.x * factor
        y = self.height / 2 - point.y * factor
        return (x, y)
