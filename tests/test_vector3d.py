import math

from geoengine.algebra.vector import Vector3D


def test_vector_addition_and_equality():
    assert Vector3D(1, 2, 3) + Vector3D(4, 5, 6) == Vector3D(5, 7, 9)


def test_norm_and_normalization():
    vector = Vector3D(3, 0, 4)
    assert vector.norm() == 5.0
    assert vector.normalized() == Vector3D(0.6, 0.0, 0.8)


def test_cross_product():
    assert Vector3D.unit_x().cross(Vector3D.unit_y()) == Vector3D.unit_z()


def test_division_by_zero_raises_value_error():
    try:
        _ = Vector3D(1, 1, 1) / 0
    except ValueError:
        return
    assert False, "Deberia haber lanzado ValueError"


def test_angle_between_orthogonal_vectors():
    angle = Vector3D.unit_x().angle_to(Vector3D.unit_y())
    assert math.isclose(angle, math.pi / 2)
