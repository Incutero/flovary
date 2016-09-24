# The number of digits of precision to use by default. You may want to set this
# to something small while debugging.
DEFAULT_PRECISION = 25

def SetDecimalPrecision(precision):
  global DEFAULT_PRECISION
  DEFAULT_PRECISION = precision


# Represents a decimal (base 10), floating-point number with a specified number
# of digits of precision.
#
# A floating-point number is a pair (significand, exponent), which represents
# the number: significand x 10^{exponent}. If this has P digits of precision,
# that means that the significand is a P-digit integer. That is, the absolute
# value of the significand is between 10^{precision-1} and 10^precision (if it
# is nonzero).
#
# All operations except division return the closest number to the mathematical
# result of the operation with the specified number of digits of precision.
#
# This class does not provide division. In order for division to be supported, a
# reciprocal function must be passed to the constructor.
#
# Implmentation Notes:
#  * This would be faster if implemented base 2 instead of base 10 for
#    some operations (e.g., shifts). However, base 10 is nicer for output.
#  * This class does not implement every operation that could conceivably be
#    provided. For example, we could add methods __lshift__ and __rshift__ for
#    supporting the shift operations (<< and >>). We could also add methods
#    __int__, __long__, and __float__ for converting decimals into these three
#    built-in types.
class Decimal(object):

  def __init__(self, value, exponent=None, precision=None, reciprocal=None):
    """Creates a new decimal from a string, integer, or its internal parts.

       A decimal can be created from a string as in Decimal('2.895e10'). This
       string must be of the form "X.XXXeYYY", where "XXX" and "YYY" can be any
       number of decimal digits. The "X.XXX" part may be preceeded by a "-" to
       indicate a negative number and the "YYY" part may be preceeded by a "-"
       to indicate a negative exponent.

       A decimal can also be created from an integer as in Decimal(15) or
       Decimal(5, precision=25). The latter form specifies the number of
       significant digits that will be stored. In the former case, the default
       number of significant digits will be kept.

       Finally, a decimal can be created from its internal parts as in
       Decimal(significand, exponent, precision). The first argument must be a
       long integer that is either 0 or has exactly precision digits. The
       resulting decimal represents the number significand * 10 ^ exponent.

       The reciprocal parameter is a function that maps a Decimal number d to
       the Decimal for 1/d. If this is not provided, then division of Decimals
       is not supported."""

    self.precision = precision or DEFAULT_PRECISION
    self.reciprocal = reciprocal

    if exponent is not None:
      # Arguments are the internal representation.
      self.significand, self.exponent = \
          Decimal._FixDigits(value, exponent, self.precision)

    elif type(value) == str:
      assert precision is None
      self.significand, self.exponent, self.precision = \
          Decimal._ParseFloatingPoint(value)
      self.significand, self.exponent = \
          Decimal._FixDigits(self.significand, self.exponent, self.precision)

    else:
      if type(value) == int:
        value = long(value)
      assert type(value) == long

      self.significand, self.exponent = \
          Decimal._FixDigits(value, 0, self.precision)

    # Always a good idea to do this before trying to use the object.
    self._CheckInvariants()

  def _CheckInvariants(self):
    """Checks that the internal representation of this object is as expected."""
    assert type(self.significand) == long
    assert type(self.exponent) == int
    assert type(self.precision) == int
    assert self.significand == 0 or \
        10L ** (self.precision - 1) <= abs(self.significand) and \
        abs(self.significand) < 10L ** self.precision
    assert self.precision >= 1

  @staticmethod
  def _FixDigits(significand, exponent, precision):
    """Returns a new significand and exponent that are shifted so that the
       precision-th digit is nonzero."""

    assert type(significand) == long
    assert type(exponent == int)

    if significand == 0:
      return 0L, 0  # no shifting is possible here

    if significand < 0:
      significand, exponent = \
          Decimal._FixDigits(-significand, exponent, precision)
      return -significand, exponent

    lower_bound = 10L ** (precision - 1)
    upper_bound = lower_bound * 10

    while significand < lower_bound:
      significand *= 10
      exponent -= 1
    while significand >= upper_bound:
      # On the very last shift, we allow rounding.
      if significand < 10 * upper_bound and significand % 10 >= 5:
        significand /= 10
        significand += 1
      else:
        significand /= 10
      exponent += 1

    return significand, exponent

  # Returns a representation of the number with fewer digits of precision.
  def shorten(self, precision):
    """Returns this number but with less precision."""
    diff = self.precision - precision
    assert diff >= 0
    if diff == 0:
       return self

    if self.significand < 0:
      return -(-self).shorten(precision)

    significand = self.significand / 10L ** diff
    exponent = self.exponent + diff

    # Round the significand up if the last digit lost was 5 or more.
    # Note that this can make the significand too big again, so we then have to
    # divide again.
    if (self.significand / 10L ** (diff - 1)) % 10 >= 5:
      significand += 1
      if significand >= 10L ** precision:
        significand /= 10L
        exponent += 1

    return Decimal(significand, exponent, precision, self.reciprocal)

  # Return a string description of the number, e.g., '1.234'.
  def __str__(self):
    return Decimal._FormatFloatingPoint(
        self.significand, self.exponent, self.precision)

  # This returns a string describing the state of the object. It may be useful
  # for debugging. A common choice is to return a string that, if evaluated as a
  # Python expression, would evaluate to an object with the same state.
  def __repr__(self):
    return 'Decimal(%d, %d, %d)' % (
        self.significand, self.exponent, self.precision)

  # The following methods convert decimals from their internal representation to
  # and from strings. The number of digits in the string, excluding the exponent
  # portion, indicates the number of digits of precision. The exponent is
  # indicated by appending "e" and then a number. Alternatively, if the exponent
  # is between 0 and precision-1, it may be indicated simply by placing the
  # decimal point in the correct position.

  @staticmethod
  def _ParseFloatingPoint(str):
    index = str.find('.')
    if index < 0:
      return long(str), 0, len(str)

    neg = False
    if str[0] == '-':
      neg = True
      str = str[1:]
    elif str[0] == '+':
      str = str[1:]

    index = str.find('e')
    if index < 0:
      index = str.find('E')
    if index >= 0:
      # A string of the form "X.XXXeYYY"
      assert str[1] == '.'
      significand = long(str[0] + str[2:index])
      exponent = int(str[index+1:]) - (index - 2)
      precision = index - 1
    else:
      # A string of the form "XXX.XXX"
      index = str.index('.')
      significand = long(str[:index] + str[index+1:])
      exponent = -(len(str) - (index + 1))
      precision = len(str) - 1

    return (-1 if neg else 1) * significand, exponent, precision

  @staticmethod
  def _FormatFloatingPoint(significand, exponent, precision):
    if significand == 0:
      if precision == 1:
        return '0'
      else:
        return '0.' + '0' * (precision - 1)
    elif significand < 0:
      return '-' + Decimal._FormatFloatingPoint(-significand,
          exponent, precision)
    else:
      s = str(significand)
      assert len(s) == precision
      if exponent + precision - 1 == 0:
        return '%s.%s' % (s[0], s[1:])
      else:
        return '%s.%se%d' % (s[0], s[1:], exponent + precision - 1)

  # The following operations are called for python code of the form "A <op> B",
  # where op is one of {+, -, *, /} and A is an instance of Decimal.
  #
  # Note that B may not be an instance of Decimal. The operations below also
  # support the case where B is an int. However, int and Decimal are the only
  # two supported cases.
  #
  # Note that we also get the operations +=, -=, *=, and /= from these.

  def __add__(self, other):
    if type(other) == int:
      other = Decimal(other, precision=self.precision)
    else:
      assert type(other) == Decimal

    if self.precision < other.precision:
      other = other.shorten(self.precision)
    if self.precision > other.precision:
      return self.shorten(other.precision).__add__(other)
    assert self.precision == other.precision

    # Special case zero because its exponent is not meaningful.
    if self.significand == 0:
      return other
    elif other.significand == 0:
      return self

    # Make sure the first argument has larger magnitude.
    if self.exponent < other.exponent:
      return other.__add__(self)

    # Find the digits of the other number when aligned to this exponent.
    exp_diff = self.exponent - other.exponent
    if exp_diff > 0:
      other_digits = other.significand / 10 ** (exp_diff)
      if (other.significand / 10 ** (exp_diff - 1)) % 10 >= 5:
        other_digits += 1
    elif exp_diff < 0:
      other_digits = other.significand * (10 ** (-exp_diff))
      if (other.significand * (10 ** (-exp_diff - 1))) % 10 >= 5:
        other_digits += 1
    else:
      other_digits = other.significand

    significand = self.significand + other_digits
    exponent = self.exponent

    # Add or remove digits so that we have exactly precision digits again.
    significand, exponent = \
        Decimal._FixDigits(significand, exponent, self.precision)
    return Decimal(significand, exponent, self.precision, self.reciprocal)

  def __sub__(self, other):
    if type(other) == int:
      other = Decimal(other, precision=self.precision)
    else:
      assert type(other) == Decimal

    return self.__add__(other.__neg__())

  def __mul__(self, other):
    if type(other) == int:
      other = Decimal(other, precision=self.precision)
    else:
      assert type(other) == Decimal

    significand = self.significand * other.significand
    exponent = self.exponent + other.exponent
    precision = min(self.precision, other.precision)

    significand, exponent = Decimal._FixDigits(significand, exponent, precision)
    return Decimal(significand, exponent, precision, self.reciprocal)

  def __div__(self, other):
    if type(other) == int:
      other = Decimal(other, precision=self.precision)
    else:
      assert type(other) == Decimal

    return self.__mul__(self.reciprocal(other))

  # The following versions are called for an operation "A <op> B", where B is an
  # instance of Decimal but A is not. As above, we allow this if A is an int.

  def __radd__(self, other):
    assert type(other) == int
    other = Decimal(other, precision=self.precision, reciprocal=self.reciprocal)
    return other.__add__(self)

  def __rsub__(self, other):
    assert type(other) == int
    other = Decimal(other, precision=self.precision, reciprocal=self.reciprocal)
    return other.__sub__(self)

  def __rmul__(self, other):
    assert type(other) == int
    other = Decimal(other, precision=self.precision, reciprocal=self.reciprocal)
    return other.__mul__(self)

  def __rdiv__(self, other):
    assert type(other) == int
    other = Decimal(other, precision=self.precision, reciprocal=self.reciprocal)
    return other.__div__(self)

  def __pow__(self, other):
    assert type(other) == int
    # Implement exponentiation by repeated squaring.
    result = Decimal(1, precision=self.precision)
    exp = 1
    pow = self
    while exp <= other:
      if exp & other <> 0:
        result = result * pow
      exp <<= 1
      pow = pow * pow
    return result

  # The following operations implement "+A", "-A", and "abs(A)".

  def __pos__(self):
    return Decimal(self.significand, self.exponent, self.precision,
        self.reciprocal)

  def __neg__(self):
    return Decimal(-self.significand, self.exponent, self.precision,
        self.reciprocal)

  def __abs__(self):
    return Decimal(abs(self.significand), self.exponent, self.precision,
        self.reciprocal)

  # The following operations implement "A <relop> B", where relop is one of
  # {==, !=, <, >, <=, >=}.
  #
  # We could equivalently implement these operations by implementing the single
  # operation __cmp__ that returns a negative number for <, zero for =, and a
  # positive number for >. Here, we handle these operations directly because we
  # want to allow equality checks between numbers with different precision (they
  # are not equal), but not <, >, <=, or += checks.

  def __eq__(self, other):
    # We require the precisions to match as well. If the precisions are
    # different, then the numbers could differ in the missing digits even if all
    # digits that are present in both are the same.
    return self.significand == other.significand and \
           self.exponent == other.exponent and \
           self.precision == other.precision

  def __ne__(self, other):
    return not self.__eq__(other)

  def __lt__(self, other):
    # Comparisons will only be supported for equal precision numbers. For
    # numbers of different precision, we cannot always answer whether one is
    # smaller or larger than the other.
    assert self.precision == other.precision

    if self.significand < 0 and other.significand >= 0:
      return True
    elif self.significand >= 0 and other.significand < 0:
      return False
    elif self.significand < 0 and other.significand < 0:
      return (-self) > (-other)  # negating inverses the relation
    else:
      if self.significand == 0:
        return other.significand <> 0
      elif other.significand == 0:
        return False
      elif self.exponent < other.exponent:
        return True
      elif self.exponent > other.exponent:
        return False
      else:
        return self.significand < other.significand

  def __gt__(self, other):
    return other.__lt__(self)

  def __le__(self, other):
    return not self.__gt__(other)

  def __ge__(self, other):
    return not self.__lt__(other)
