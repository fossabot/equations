#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Eisenstein Rational Fractions Type Implementation - Python 3.x
   Copyright (c) 2019 Michal Widera

   Defined operations on Eisenstein integers:
   https://en.wikipedia.org/wiki/Eisenstein_integer
"""

# https://docs.python.org/3.7/reference/datamodel.html

SQRT_THREE: float = 3.0 ** 0.5


def upgrade_number(other):
    """
    This function will upgrade argument to Eisenstein

    :param other: int, Eisenstein
    :return:  same value but Eisenstein type
    """
    if isinstance(other, int):
        other = Eisenstein(other, 0)
    return other


class Eisenstein:
    def __init__(self, a, b=0):

        if isinstance(a, int) and isinstance(b, int):
            self.a = a
            self.b = b
        else:
            raise TypeError("arguments should be an int")

    def __repr__(self):
        return "(%s, %sw)" % (self.a, self.b)

    def __eq__(self, other):
        other = upgrade_number(other)
        return self.a == other.a and self.b == other.b

    def __add__(self, other):
        other = upgrade_number(other)
        return Eisenstein(self.a + other.a, self.b + other.b)

    def __sub__(self, other):
        other = upgrade_number(other)
        return Eisenstein(self.a - other.a, self.b - other.b)

    def __mul__(self, other):
        # (a+bw)(c+dw)=(ac-bd)+(bc+ad-db)w
        # https://en.wikipedia.org/wiki/Eisenstein_integer
        other = upgrade_number(other)

        return Eisenstein(
            (self.a * other.a) - (self.b * other.b),
            (self.b * other.a) + (self.a * other.b) - (self.b * other.b),
        )

    def __abs__(self):
        # |a+bw|^2 = a*a - a*b + b*b
        # https://en.wikipedia.org/wiki/Eisenstein_integer
        return (self.a ** 2 - self.a * self.b + self.b ** 2) ** 0.5

    __rmul__ = __mul__
    __radd__ = __add__

    @property
    def get_complex_form(self) -> complex:
        """
        (a,bw)->(x,iy), where x,y: float, a,b: integer
        :return: Complex number from Eisenstein
        """
        return complex(self.a - (self.b / 2), (self.b * SQRT_THREE) / 2)

    @property
    def get_norm(self):
        """
        wolframalfa
        query: w = ( -1 + i sqrt(3) ) / 2 ; ( a + b w^2 ) ( a + b w )
        answer: a^2 - ab + b^2

        :return: Norm in algebraic sense
        """
        return self.a ** 2 - self.a * self.b + self.b ** 2

    def __floordiv__(self, other):
        other = upgrade_number(other)
        return get_eisenstein_form(self.get_complex_form / other.get_complex_form)

    def __mod__(self, other):
        other = upgrade_number(other)

        K = get_eisenstein_form(self.get_complex_form / other.get_complex_form)
        # This debug code is important - it creates queries for
        # wolframalfa that can be checked if mod function works correctly

        # print(
        #    # self = K * other + R
        #    'w = ( -1 + i sqrt(3) ) / 2 ; %r %r + %r ; expected %r'
        #    % (K, other, self - K * other, self)
        # )

        return self - K * other


def get_dot_product(x: Eisenstein, y: Eisenstein):
    """
    Dot product
    https://www.quora.com/What-is-dot-product-of-two-complex-numbers
    google: "if dot product is zero" -> angle 90 degrees

    :return: dot product of two complex numbers
    """

    val1 = x.get_complex_form
    val2 = y.get_complex_form
    return val1.real * val2.real + val1.imag * val2.imag


def get_eisenstein_form(var: complex):
    """
    (x,iy) -> (a,bw), where x,y: float, a,b: integer
    :return: Eisenstein number from complex
    """
    x = var.real
    y = var.imag
    return Eisenstein(round(x + y / SQRT_THREE), round((2 * y) / SQRT_THREE))


def gcd(x: Eisenstein, y: Eisenstein):
    """Calculate the Greatest Common Divisor of a and b.

    Paper: Efficient algorithms for gcd and cubic residuosity
           in the ring of Eisenstein integers
    http://cs.au.dk/~gudmund/Documents/cubicres.pdf

    Unless b==0, the result will have the same sign as b (so that when
    b is divided by it, the result comes out positive).
    """

    if abs(y) > abs(x):
        x, y = y, x
    while get_dot_product(x, y):
        x, y = y, x % y
    return x
