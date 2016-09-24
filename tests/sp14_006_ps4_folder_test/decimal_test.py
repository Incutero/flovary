from decimal import Decimal, SetDecimalPrecision
from math import ceil, log10
from sys import argv

import unittest


SetDecimalPrecision(4)


class DecimalTest(unittest.TestCase):

  def test_string_conversion(self):
    self.assertEquals(str(Decimal('1.234')), '1.234')
    self.assertEquals(str(Decimal('1234')), '1.234e3')
    self.assertEquals(str(Decimal('1.000')), '1.000')
    self.assertEquals(str(Decimal('-1.234')), '-1.234')
    self.assertEquals(str(Decimal('+1.234')), '1.234')

  def test_int_creation(self):
    self.assertEquals(str(Decimal(0)), '0.000')
    self.assertEquals(str(Decimal(1)), '1.000')
    self.assertEquals(str(Decimal(-1)), '-1.000')
    self.assertEquals(str(Decimal(1234)), '1.234e3')

  def test_int_creation_with_digits(self):
    self.assertEquals(str(Decimal(0, precision=1)), '0')
    self.assertEquals(str(Decimal(1, precision=1)), '1.')
    self.assertEquals(str(Decimal(-1, precision=1)), '-1.')

    self.assertEquals(str(Decimal(0, precision=2)), '0.0')
    self.assertEquals(str(Decimal(1, precision=2)), '1.0')
    self.assertEquals(str(Decimal(-1, precision=2)), '-1.0')

    self.assertEquals(str(Decimal(0, precision=5)), '0.0000')
    self.assertEquals(str(Decimal(1, precision=5)), '1.0000')
    self.assertEquals(str(Decimal(-1, precision=5)), '-1.0000')

    self.assertEquals(str(Decimal(1234, precision=1)), '1.e3')
    self.assertEquals(str(Decimal(1234, precision=2)), '1.2e3')
    self.assertEquals(str(Decimal(1234, precision=3)), '1.23e3')
    self.assertEquals(str(Decimal(1234, precision=4)), '1.234e3')
    self.assertEquals(str(Decimal(1234, precision=5)), '1.2340e3')
    self.assertEquals(str(Decimal(1234, precision=8)), '1.2340000e3')

  def test_creation_from_internal_representation(self):
    self.assertEquals(str(Decimal(0L, 0, 2)), '0.0')
    self.assertEquals(str(Decimal(10L, -2, 2)), '1.0e-1')
    self.assertEquals(str(Decimal(10L, -1, 2)), '1.0')
    self.assertEquals(str(Decimal(15L, -1, 2)), '1.5')
    self.assertEquals(str(Decimal(-10L, -2, 2)), '-1.0e-1')
    self.assertEquals(str(Decimal(-10L, -1, 2)), '-1.0')

    self.assertEquals(str(Decimal(1234L, 2, 4)), '1.234e5')
    self.assertEquals(str(Decimal(1234L, 1, 4)), '1.234e4')
    self.assertEquals(str(Decimal(1234L, 0, 4)), '1.234e3')
    self.assertEquals(str(Decimal(1234L, -1, 4)), '1.234e2')
    self.assertEquals(str(Decimal(1234L, -2, 4)), '1.234e1')
    self.assertEquals(str(Decimal(1234L, -3, 4)), '1.234')
    self.assertEquals(str(Decimal(1234L, -4, 4)), '1.234e-1')
    self.assertEquals(str(Decimal(1234L, -5, 4)), '1.234e-2')

  def test_add(self):
    self.assertEquals(str(Decimal(1) + Decimal(2)), '3.000')
    self.assertEquals(str(Decimal('1.23') + Decimal('1.00')), '2.23')
    self.assertEquals(str(Decimal('1.23') + Decimal('0.77')), '2.00')
    self.assertEquals(str(Decimal('1.23') + Decimal('-0.23')), '1.00')
    self.assertEquals(
        str(Decimal(1435267, precision=7) +
            Decimal(2349834, precision=7)), '3.785101e6')

    self.assertEquals(str(Decimal('1.23') + 0), '1.23')
    self.assertEquals(str(Decimal('1.23') + 1), '2.23')
    self.assertEquals(str(Decimal('1.23') + -1), '2.30e-1')
    self.assertEquals(str(Decimal('1.23') + -2), '-7.70e-1')

    self.assertEquals(str(Decimal('1.23') + Decimal('1.0')), '2.2')
    self.assertEquals(str(Decimal('1.23') + Decimal('-1.0')), '2.0e-1')
    self.assertEquals(str(Decimal('1.25') + Decimal('1.0')), '2.3')
    self.assertEquals(str(Decimal('1.2499') + Decimal('1.0')), '2.2')

    self.assertEquals(str(0 + Decimal('1.23')), '1.23')
    self.assertEquals(str(1 + Decimal('1.23')), '2.23')
    self.assertEquals(str(-1 + Decimal('1.23')), '2.30e-1')
    self.assertEquals(str(-2 + Decimal('1.23')), '-7.70e-1')

  def test_sub(self):
    self.assertEquals(str(Decimal(1) - Decimal(2)), '-1.000')
    self.assertEquals(str(Decimal('1.23') - Decimal('1.00')), '2.30e-1')
    self.assertEquals(str(Decimal('1.23') - Decimal('0.77')), '4.60e-1')
    self.assertEquals(str(Decimal('1.23') - Decimal('-0.23')), '1.46')
    self.assertEquals(
        str(Decimal(1435267, precision=7) - Decimal(2349834, precision=7)),
        '-9.145670e5')

    self.assertEquals(str(Decimal('1.23') - 0), '1.23')
    self.assertEquals(str(Decimal('1.23') - 1), '2.30e-1')
    self.assertEquals(str(Decimal('1.23') - -1), '2.23')
    self.assertEquals(str(Decimal('1.23') - -2), '3.23')

    self.assertEquals(str(Decimal('1.23') - Decimal('1.0')), '2.0e-1')
    self.assertEquals(str(Decimal('1.23') - Decimal('-1.0')), '2.2')
    self.assertEquals(str(Decimal('1.25') - Decimal('1.0')), '3.0e-1')
    self.assertEquals(str(Decimal('1.2499') - Decimal('1.0')), '2.0e-1')
    self.assertEquals(str(Decimal('1.2500') - Decimal('1.0')), '3.0e-1')

    self.assertEquals(str(Decimal('1.2') - Decimal('1.03')), '2.0e-1')
    self.assertEquals(str(Decimal('1.2') - Decimal('1.05')), '1.0e-1')

    self.assertEquals(str(0 - Decimal('1.23')), '-1.23')
    self.assertEquals(str(1 - Decimal('1.23')), '-2.30e-1')
    self.assertEquals(str(-1 - Decimal('1.23')), '-2.23')
    self.assertEquals(str(-2 - Decimal('-1.23')), '-7.70e-1')

  def test_mul(self):
    self.assertEquals(str(Decimal('1.23') * Decimal('1.00')), '1.23')
    self.assertEquals(str(Decimal('1.23') * Decimal('0.00')), '0.00')
    self.assertEquals(str(Decimal('1.23') * Decimal('3.00')), '3.69')
    self.assertEquals(str(Decimal('1.00') * Decimal('1.23')), '1.23')
    self.assertEquals(str(Decimal('0.00') * Decimal('1.23')), '0.00')
    self.assertEquals(str(Decimal('5.00') * Decimal('1.23')), '6.15')

    self.assertEquals(str(Decimal('5.00') * Decimal('1.23')), '6.15')
    self.assertEquals(str(Decimal('5.00') * Decimal('1.23')), '6.15')
    self.assertEquals(str(Decimal('5.00') * Decimal('1.23')), '6.15')

    self.assertEquals(str(Decimal('5.434') * Decimal('4.618')), '2.509e1')
    self.assertEquals(str(Decimal('1.559') * Decimal('1.525')), '2.377')
    self.assertEquals(str(Decimal('3.341') * Decimal('5.291')), '1.768e1')
    self.assertEquals(str(Decimal('2.620') * Decimal('4.826')), '1.264e1')
    self.assertEquals(str(Decimal('9.614') * Decimal('6.770')), '6.509e1')

    self.assertEquals(
        str(Decimal('558299.24682') * Decimal('568426.55554')),
        '3.1735211783e11')
    self.assertEquals(
        str(Decimal('751619.603736') * Decimal('4470008.565551')),
        '3.35974606674e12')

    self.assertEquals(str(Decimal('1.23') * Decimal('-1.00')), '-1.23')
    self.assertEquals(str(Decimal('-1.23') * Decimal('1.00')), '-1.23')
    self.assertEquals(str(Decimal('-1.23') * Decimal('-3.00')), '3.69')

    self.assertEquals(str(Decimal('1.23') * 1), '1.23')
    self.assertEquals(str(Decimal('1.23') * 0), '0.00')
    self.assertEquals(str(Decimal('1.23') * 3), '3.69')
    self.assertEquals(str(1 * Decimal('1.23')), '1.23')
    self.assertEquals(str(0 * Decimal('1.23')), '0.00')
    self.assertEquals(str(5 * Decimal('1.23')), '6.15')

    self.assertEquals(str(Decimal('5.434') * Decimal('4.0')), '2.2e1')
    self.assertEquals(str(Decimal('1.559') * Decimal('1.5')), '2.3')
    self.assertEquals(str(Decimal('3.341') * Decimal('5.29')), '1.77e1')

  def test_assign_op(self):
    a = Decimal('1.23')
    self.assertEquals(str(a + Decimal('0.01')), '1.24')
    self.assertEquals(str(a), '1.23')
    a += Decimal('0.02')
    self.assertEquals(str(a), '1.25')
    a -= Decimal('0.02')
    self.assertEquals(str(a), '1.23')
    a *= Decimal('2.94')
    self.assertEquals(str(a), '3.62')

  def test_pow(self):
    self.assertEquals(str(Decimal(2) ** 0), '1.000')
    self.assertEquals(str(Decimal(2) ** 1), '2.000')
    self.assertEquals(str(Decimal(2) ** 2), '4.000')
    self.assertEquals(str(Decimal(2) ** 3), '8.000')
    self.assertEquals(str(Decimal(2) ** 4), '1.600e1')
    self.assertEquals(str(Decimal(2) ** 5), '3.200e1')
    self.assertEquals(str(Decimal(2) ** 6), '6.400e1')
    self.assertEquals(str(Decimal(2) ** 7), '1.280e2')
    self.assertEquals(str(Decimal(2) ** 8), '2.560e2')
    self.assertEquals(str(Decimal(2) ** 9), '5.120e2')

  def test_pos_neg(self):
    self.assertEquals(str(+Decimal(0)), '0.000')
    self.assertEquals(str(+Decimal('1.23')), '1.23')
    self.assertEquals(str(+Decimal('-1.23')), '-1.23')
    self.assertEquals(str(-Decimal(0)), '0.000')
    self.assertEquals(str(-Decimal('1.23')), '-1.23')
    self.assertEquals(str(-Decimal('-1.23')), '1.23')

  def test_abs(self):
    self.assertEquals(str(abs(Decimal(0))), '0.000')
    self.assertEquals(str(abs(Decimal('1.23'))), '1.23')
    self.assertEquals(str(abs(Decimal('-1.23'))), '1.23')

  def test_equality(self):
    self.assertEquals(Decimal(0), Decimal(0))
    self.assertEquals(Decimal(1), Decimal(1))
    self.assertEquals(Decimal(-1), Decimal(-1))
    self.assertNotEquals(Decimal(0), Decimal(1))
    self.assertNotEquals(Decimal(0), Decimal(-1))
    self.assertNotEquals(Decimal(1), Decimal(-1))

    self.assertEquals(Decimal(1234, precision=4), Decimal(1234, precision=4))
    self.assertNotEquals(Decimal(1235, precision=4), Decimal(1234, precision=4))

  def test_comparison(self):
    self.assertFalse(Decimal(0) < Decimal(0))
    self.assertFalse(Decimal(0) > Decimal(0))
    self.assertTrue(Decimal(0) <= Decimal(0))
    self.assertTrue(Decimal(0) >= Decimal(0))

    self.assertTrue(Decimal(0) < Decimal(1))
    self.assertFalse(Decimal(0) > Decimal(1))
    self.assertTrue(Decimal(0) <= Decimal(1))
    self.assertFalse(Decimal(0) >= Decimal(1))

    self.assertFalse(Decimal(0) < Decimal(-1))
    self.assertTrue(Decimal(0) > Decimal(-1))
    self.assertFalse(Decimal(0) <= Decimal(-1))
    self.assertTrue(Decimal(0) >= Decimal(-1))

    self.assertFalse(Decimal(1) < Decimal(-1))
    self.assertTrue(Decimal(1) > Decimal(-1))
    self.assertFalse(Decimal(1) <= Decimal(-1))
    self.assertTrue(Decimal(1) >= Decimal(-1))

    self.assertTrue(Decimal('1.234') < Decimal('1.235'))
    self.assertFalse(Decimal('1.234') > Decimal('1.235'))
    self.assertTrue(Decimal('1.234') <= Decimal('1.235'))
    self.assertFalse(Decimal('1.234') >= Decimal('1.235'))


if __name__ == '__main__':
  unittest.main()
