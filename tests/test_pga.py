from tfga import GeometricAlgebra
import unittest as ut
import tensorflow as tf

# Make tensorflow not take over the entire GPU memory
for gpu in tf.config.experimental.list_physical_devices('GPU'):
    tf.config.experimental.set_memory_growth(gpu, True)


pga_signature = [0, 1, 1, 1]


class TestDualGeometricAlgebraMultiply(ut.TestCase):
    def assertTensorsApproxEqual(self, a, b, tolerance=1e-4):
        self.assertTrue(tf.reduce_all(tf.abs(a - b) < tolerance),
                        "%s not equal to %s" % (a, b))

    def test_exp_eq_approx_exp_e01_e02(self):
        pga = GeometricAlgebra(pga_signature)

        # a = 3e01 + 5e02
        a = 3 * pga.e01 + 5 * pga.e02

        # exp(a) = 1 + 3e01 + 5e02
        self.assertTensorsApproxEqual(pga.approx_exp(a), pga.exp(a))

    def test_exp_eq_approx_exp_e12_e23(self):
        pga = GeometricAlgebra(pga_signature)

        # a = 3e12 + 5e23
        a = 3 * pga.e12 + 5 * pga.e23

        # exp(a) ~= 0.90 - 0.22e12 -0.37e23
        self.assertTensorsApproxEqual(pga.approx_exp(a), pga.exp(a))

    def test_inverse(self):
        pga = GeometricAlgebra(pga_signature)

        # a = 3e12 + 5e23
        a = 3 * pga.e12 + 5 * pga.e23

        # a_inv: -0.09*e_12 + -0.15*e_23
        a_inv = pga.inverse(a)

        # a a_inv should be 1
        self.assertTensorsApproxEqual(pga.geom_prod(a, a_inv), 1 * pga.e(""))
