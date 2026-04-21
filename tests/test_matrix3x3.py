import math

from geoengine.algebra.matrix import Matrix3x3
from geoengine.algebra.vector import Vector3D


def test_rotation_z_rotates_x_axis_into_y_axis():
    matrix = Matrix3x3.rotation_z(math.pi / 2)
    result = matrix * Vector3D.unit_x()
    assert result == Vector3D(0.0, 1.0, 0.0)


def test_matrix_multiplication_and_inverse():
    matrix = Matrix3x3.from_euler(0.2, 0.3, 0.4) * Matrix3x3.scale(1.2, 0.8, 1.1)
    identity = matrix * matrix.inverse()

    for row_index in range(3):
        for column_index in range(3):
            expected = 1.0 if row_index == column_index else 0.0
            assert math.isclose(identity.data[row_index][column_index], expected, abs_tol=1e-7)


def test_determinant_of_scale_matrix():
    matrix = Matrix3x3.scale(2.0, 3.0, 4.0)
    assert matrix.determinant() == 24.0
