from decimal import Decimal


# Returns the next guess after one iteration of Newton's method.
#
# Arguments:
#  - number: The number whose cube root is to be calculated.
#  - guess: The current guess of the cube root.
def CubeRootNewtonIteration(number, guess):
  assert type(number) == int

  # BEGIN STUDENT CODE
  raise NotImplementedError()
  # END STUDENT CODE


# Returns an integer guess for the cube root of the number.
#
# Arguments:
# - number: The number whose cube root is to be calculated.
def CubeRootGuess(number):
  assert type(number) == int

  # BEGIN STUDENT CODE
  raise NotImplementedError()
  # END STUDENT CODE


# Returns the best floating-point approximation to the cube root of the number.
#
# Arguments:
# - number: The number whose cube root is to be calculated.
def FloatCubeRoot(number):
  assert type(number) == int

  # BEGIN STUDENT CODE
  raise NotImplementedError()
  # END STUDENT CODE


# Returns a guess of the reciprocal of the given decimal number.
#
# Arguments:
# - number: The decimal number whose reciprocal is to be guessed.
def ReciprocalGuess(number):
  assert type(number) == Decimal

  # BEGIN STUDENT CODE
  raise NotImplementedError()
  # END STUDENT CODE


# Returns the reciprocal of the give decimal number, computed to the same
# precision as number itself (i.e., number.precision).
#
# Arguments:
# - number: The decimal number whose reciprocal is to be computed.
def DecimalReciprocal(number):
  assert type(number) == Decimal

  # BEGIN STUDENT CODE
  raise NotImplementedError()
  # END STUDENT CODE


# Returns the best approximation to the cube root of the number using decimal
# numbers with the given number of digits of precision.
#
# Arguments:
# - number: The number whose cube root is to be calculated.
# - precision: The number of digits of precision to use.
def DecimalCubeRoot(number, precision):
  assert type(number) == int
  assert type(precision) == int

  # Note: You will need to pass reciprocal=DecimalReciprocal when creating
  #       Decimal numbers with support for division.

  # BEGIN STUDENT CODE
  raise NotImplementedError()
  # END STUDENT CODE
