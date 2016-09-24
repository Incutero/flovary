import PSET4
import sys

from decimal import Decimal


#
# Test Helper Routines
#

# Check whether part of PSET4 has been implemented yet.
def IsImplemented(func, args):
  try:
    func(*args)
    return True
  except NotImplementedError:
    return False

# Check that the cube root guess is reasonable.
def CheckCubeRootGuess(number, guess):
  assert type(number) == int
  assert type(guess) == int

  rel_error = abs(guess**3 - number) / number
  if rel_error < 2:
    print "Reasonable guess for cube root of %d" % (number,)
  else:
    print "Poor guess for cube root of %d: %.16f" % (number, guess)
    sys.exit(1)

# Check the accuracy of a floating-point cube root.
def CheckFloatCubeRoot(number, guess):
  assert type(number) == int
  assert type(guess) == float

  rel_error = abs(guess**3 - number) / number
  if rel_error < 1e-15:
    print "%.15f^3 == %d to 15 digits." % (guess, number)
  elif rel_error < 1e-14:
    print "%.15f^3 == %d to 14 digits." % (guess, number)
  elif rel_error < 1e-13:
    print "%.15f^3 == %d to 13 digits." % (guess, number)
  elif rel_error < 1e-12:
    print "%.15f^3 == %d to 12 digits." % (guess, number)
  elif rel_error < 1e-11:
    print "%.15f^3 == %d to 11 digits." % (guess, number)
  elif rel_error < 1e-10:
    print "%.15f^3 == %d to 10 digits." % (guess, number)
  else:
    print "Incorrect cube root of %d: %.16f" % (number, guess)
    sys.exit(1)

# Check that the reciprocal guess is reasonable.
def CheckReciprocalGuess(number, answer):
  assert type(number) == Decimal
  assert type(answer) == Decimal
  assert number.precision == answer.precision

  guess = PSET4.ReciprocalGuess(number)
  if guess <= 2 * answer and answer <= 2 * guess:
    print "Reasonable guess for 1 / %s" % (number,)
  else:
    print "Poor guess for 1 / %s: %s" % (number, guess)
    sys.exit(1)

# Check that the computed reciprocal is correct to the given tolerance.
def CheckDecimalReciprocal(number, answer, max_error):
  assert type(number) == Decimal
  assert type(answer) == Decimal
  assert type(max_error) == Decimal

  guess = PSET4.DecimalReciprocal(number)
  if abs(guess - answer) <= max_error:
    print "Correct value for 1 / %s" % (number,)
  else:
    print "Incorrect value for 1 / %s: %s" % (number, guess)
    sys.exit(1)

# Check the accuracy of a Decimal cube root.
def CheckDecimalCubeRoot(number, guess, precision):
  assert type(number) == int
  assert type(guess) == Decimal

  result = guess ** 3
  error = Decimal(long(number), 1 - precision, precision)
  if abs(guess ** 3 - number) <= error * number:
    print "Correct cube root of %d (to %d digits): %s" % (
        number, precision, guess)
  else:
    print "Incorrect cube root of %d: %s" % (number, guess)
    sys.exit(1)


#
# Tests
#

print
print "Part (a): Computing the cube root of 7..."
print

if IsImplemented(PSET4.CubeRootNewtonIteration, (7, 2.0)):
  print "Starting with a good guess (2):"

  guess = 2.0
  for i in range(0, 6):
    guess = PSET4.CubeRootNewtonIteration(7, guess)
    print "  iteration %2d: %.16f" % (i+1, guess)

  CheckFloatCubeRoot(7, guess)

  print
  print "Starting with a bad guess (1000000):"

  guess = 1000000.0
  for i in range(0, 39):
    guess = PSET4.CubeRootNewtonIteration(7, guess)
    print "  iteration %2d: %.16f" % (i+1, guess)

  CheckFloatCubeRoot(7, guess)
else:
  print "CubeRootNewtonIteration is not yet implemented"
  sys.exit(0)


print
print
print "Part (b): Computing the cube root of \"y\"..."
print

if IsImplemented(PSET4.CubeRootGuess, (2,)):
  CheckCubeRootGuess(2, PSET4.CubeRootGuess(2))
  CheckCubeRootGuess(11, PSET4.CubeRootGuess(11))
  CheckCubeRootGuess(26, PSET4.CubeRootGuess(26))
  CheckCubeRootGuess(297, PSET4.CubeRootGuess(297))
  CheckCubeRootGuess(1533, PSET4.CubeRootGuess(1533))
else:
  print "CubeRootGuess is not yet implemented"
  sys.exit(0)

print
if IsImplemented(PSET4.FloatCubeRoot, (2,)):
  CheckFloatCubeRoot(2, PSET4.FloatCubeRoot(2))
  CheckFloatCubeRoot(11, PSET4.FloatCubeRoot(11))
  CheckFloatCubeRoot(26, PSET4.FloatCubeRoot(26))
  CheckFloatCubeRoot(297, PSET4.FloatCubeRoot(297))
  CheckFloatCubeRoot(1533, PSET4.FloatCubeRoot(1533))
else:
  print "FloatCubeRoot is not yet implemented"
  sys.exit(0)


print
print
print "Part (c): Computing reciprocal to arbitrary precision..."
print

if IsImplemented(PSET4.ReciprocalGuess, (Decimal(1),)):
  CheckReciprocalGuess(Decimal('1.00000'), Decimal('1.00000'))
  CheckReciprocalGuess(Decimal('2.00000'), Decimal('5.00000e-1'))
  CheckReciprocalGuess(Decimal('9.00000'), Decimal('1.11111e-1'))
  CheckReciprocalGuess(Decimal('10.0000'), Decimal('1.00000e-1'))
  CheckReciprocalGuess(Decimal('19.0000'), Decimal('5.26316e-2'))
  CheckReciprocalGuess(Decimal('99.0000'), Decimal('1.01010e-2'))
  CheckReciprocalGuess(Decimal('100.000'), Decimal('1.00000e-2'))
  CheckReciprocalGuess(Decimal('999.000'), Decimal('1.00100e-3'))
  CheckReciprocalGuess(Decimal('1000.00'),  Decimal('1.00000e-3'))

  CheckReciprocalGuess(Decimal('0.10000'), Decimal('1.00000e1'))
  CheckReciprocalGuess(Decimal('0.01000'), Decimal('1.00000e2'))
  CheckReciprocalGuess(Decimal('0.00100'), Decimal('1.00000e3'))
  CheckReciprocalGuess(Decimal('0.99900'), Decimal('1.00100'))
  CheckReciprocalGuess(Decimal('0.99000'), Decimal('1.01010'))
  CheckReciprocalGuess(Decimal('0.90000'), Decimal('1.11111'))
  CheckReciprocalGuess(Decimal('0.09900'), Decimal('1.01010e1'))
  CheckReciprocalGuess(Decimal('0.09000'), Decimal('1.11111e1'))
  CheckReciprocalGuess(Decimal('0.00900'), Decimal('1.11111e2'))

  CheckReciprocalGuess(Decimal('6.873'), Decimal('1.455e-1'))
  CheckReciprocalGuess(Decimal('8.133'), Decimal('1.230e-1'))
  CheckReciprocalGuess(Decimal('16.127'), Decimal('6.2008e-2'))
  CheckReciprocalGuess(Decimal('35.554'), Decimal('2.8126e-2'))
  CheckReciprocalGuess(Decimal('141.638'), Decimal('7.06025e-3'))
  CheckReciprocalGuess(Decimal('270.337'), Decimal('3.69909e-3'))

  CheckReciprocalGuess(Decimal('0.062'), Decimal('1.613e1'))
  CheckReciprocalGuess(Decimal('0.085'), Decimal('1.176e1'))
  CheckReciprocalGuess(Decimal('0.0281'), Decimal('3.5587e1'))
  CheckReciprocalGuess(Decimal('0.0881'), Decimal('1.1351e1'))
  CheckReciprocalGuess(Decimal('0.12296'), Decimal('8.13273'))
  CheckReciprocalGuess(Decimal('0.32476'), Decimal('3.07920'))

  # Try some numbers so big they can't be converted to a float.
  CheckReciprocalGuess(Decimal('1.000e1000'), Decimal('1.000e-1000'))
  CheckReciprocalGuess(Decimal('5.000e-1000'), Decimal('2.000e999'))
else:
  print "ReciprocalGuess is not yet implemented"
  sys.exit(0)

print
if IsImplemented(PSET4.DecimalReciprocal, (Decimal(1),)):
  max_err = Decimal('0.00010')
  CheckDecimalReciprocal(Decimal('1.00000'), Decimal('1.00000'), max_err)
  CheckDecimalReciprocal(Decimal('2.00000'), Decimal('5.00000e-1'), max_err)
  CheckDecimalReciprocal(Decimal('9.00000'), Decimal('1.11111e-1'), max_err)
  CheckDecimalReciprocal(Decimal('10.0000'), Decimal('1.00000e-1'), max_err)
  CheckDecimalReciprocal(Decimal('19.0000'), Decimal('5.26316e-2'), max_err)
  CheckDecimalReciprocal(Decimal('99.0000'), Decimal('1.01010e-2'), max_err)
  CheckDecimalReciprocal(Decimal('100.000'), Decimal('1.00000e-2'), max_err)
  CheckDecimalReciprocal(Decimal('999.000'), Decimal('1.00100e-3'), max_err)
  CheckDecimalReciprocal(Decimal('1000.00'), Decimal('1.00000e-3'), max_err)

  CheckDecimalReciprocal(Decimal('0.10000'), Decimal('1.00000e1'), max_err)
  CheckDecimalReciprocal(Decimal('0.01000'), Decimal('1.00000e2'), max_err)
  CheckDecimalReciprocal(Decimal('0.00100'), Decimal('1.00000e3'), max_err)
  CheckDecimalReciprocal(Decimal('0.99900'), Decimal('1.00100'), max_err)
  CheckDecimalReciprocal(Decimal('0.99000'), Decimal('1.01010'), max_err)
  CheckDecimalReciprocal(Decimal('0.90000'), Decimal('1.11111'), max_err)
  CheckDecimalReciprocal(Decimal('0.09900'), Decimal('1.01010e1'), max_err)
  CheckDecimalReciprocal(Decimal('0.09000'), Decimal('1.11111e1'), max_err)
  CheckDecimalReciprocal(Decimal('0.00900'), Decimal('1.11111e2'), max_err)

  max_err = Decimal('0.010')
  CheckDecimalReciprocal(Decimal('6.873'), Decimal('1.455e-1'), max_err)
  CheckDecimalReciprocal(Decimal('8.133'), Decimal('1.230e-1'), max_err)
  max_err = Decimal('0.0010')
  CheckDecimalReciprocal(Decimal('16.127'), Decimal('6.2008e-2'), max_err)
  CheckDecimalReciprocal(Decimal('35.554'), Decimal('2.8126e-2'), max_err)
  max_err = Decimal('0.00010')
  CheckDecimalReciprocal(Decimal('141.638'), Decimal('7.06025e-3'), max_err)
  CheckDecimalReciprocal(Decimal('270.337'), Decimal('3.69909e-3'), max_err)

  max_err = Decimal('0.010')
  CheckDecimalReciprocal(Decimal('0.062'), Decimal('1.613e1'), max_err)
  CheckDecimalReciprocal(Decimal('0.085'), Decimal('1.176e1'), max_err)
  max_err = Decimal('0.0010e1')
  CheckDecimalReciprocal(Decimal('0.0281'), Decimal('3.5587e1'), max_err)
  CheckDecimalReciprocal(Decimal('0.0881'), Decimal('1.1351e1'), max_err)
  max_err = Decimal('0.00010')
  CheckDecimalReciprocal(Decimal('0.12296'), Decimal('8.13273'), max_err)
  CheckDecimalReciprocal(Decimal('0.32476'), Decimal('3.07920'), max_err)

  max_err = Decimal('0.010e-1000')
  CheckDecimalReciprocal(Decimal('1.000e1000'), Decimal('1.000e-1000'), max_err)
  max_err = Decimal('0.010e999')
  CheckDecimalReciprocal(Decimal('5.000e-1000'), Decimal('2.000e999'), max_err)
else:
  print "DecimalReciprocal is not yet implemented"
  sys.exit(0)


print
print
print "Part (d): Computing the cube root of \"y\" to arbitrary precision..."
print

if IsImplemented(PSET4.DecimalCubeRoot, (2, 10)):
  # First, try 10 digits of precision.
  CheckDecimalCubeRoot(2, PSET4.DecimalCubeRoot(2, 10), 10)
  CheckDecimalCubeRoot(11, PSET4.DecimalCubeRoot(11, 10), 10)
  CheckDecimalCubeRoot(26, PSET4.DecimalCubeRoot(26, 10), 10)
  CheckDecimalCubeRoot(297, PSET4.DecimalCubeRoot(297, 10), 10)
  CheckDecimalCubeRoot(1533, PSET4.DecimalCubeRoot(1533, 10), 10)

  # Now, try 100 digits of precision.
  CheckDecimalCubeRoot(2, PSET4.DecimalCubeRoot(2, 100), 100)
  CheckDecimalCubeRoot(11, PSET4.DecimalCubeRoot(11, 100), 100)
  CheckDecimalCubeRoot(26, PSET4.DecimalCubeRoot(26, 100), 100)
  CheckDecimalCubeRoot(297, PSET4.DecimalCubeRoot(297, 100), 100)
  CheckDecimalCubeRoot(1533, PSET4.DecimalCubeRoot(1533, 100), 100)

  # Finally, try 1000 digits of precision.
  CheckDecimalCubeRoot(2, PSET4.DecimalCubeRoot(2, 1000), 1000)
  CheckDecimalCubeRoot(11, PSET4.DecimalCubeRoot(11, 1000), 1000)
  CheckDecimalCubeRoot(26, PSET4.DecimalCubeRoot(26, 1000), 1000)
  CheckDecimalCubeRoot(297, PSET4.DecimalCubeRoot(297, 1000), 1000)
  CheckDecimalCubeRoot(1533, PSET4.DecimalCubeRoot(1533, 1000), 1000)
else:
  print "DecimalReciprocal is not yet implemented"
  sys.exit(0)
