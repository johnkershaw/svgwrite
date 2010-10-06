#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: test full11typechecker
# Created: 04.10.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import sys
import unittest

from svgwrite.data.full11typechecker import Full11TypeChecker

class TestFull11TypeChecker(unittest.TestCase):
    def setUp(self):
        self.checker = Full11TypeChecker()

    def test_is_anything(self):
        """ Everything is valid. """
        self.assertTrue(self.checker.is_anything('abcdef  :::\n \r \t all is valid äüß'))
        self.assertTrue(self.checker.is_anything(100.0))
        self.assertTrue(self.checker.is_anything((100.0, 11)))
        self.assertTrue(self.checker.is_anything(dict(a=100, b=200)))

    def test_is_string(self):
        """ Everything is valid. """
        self.assertTrue(self.checker.is_anything('abcdef  :::\n \r \t all is valid äüß'))
        self.assertTrue(self.checker.is_anything(100.0))
        self.assertTrue(self.checker.is_anything((100.0, 11)))
        self.assertTrue(self.checker.is_anything(dict(a=100, b=200)))

    def test_is_number(self):
        """ Integer and Float, also as String '100' or '3.1415'. """
        # big numbers only valid for full profile
        self.assertTrue(self.checker.is_number(100000))
        self.assertTrue(self.checker.is_number(-100000))
        self.assertTrue(self.checker.is_number(3.141592))
        self.assertTrue(self.checker.is_number('100000'))
        self.assertTrue(self.checker.is_number('-100000'))
        self.assertTrue(self.checker.is_number('3.141592'))
    def test_is_not_number(self):
        self.assertFalse(self.checker.is_number( (1,2) ))
        self.assertFalse(self.checker.is_number('manfred'))
        self.assertFalse(self.checker.is_number( dict(a=1, b=2) ))

    def test_is_name(self):
        self.assertTrue(self.checker.is_name('mozman-öäüß'))
        self.assertTrue(self.checker.is_name('mozman:mozman'))
        self.assertTrue(self.checker.is_name('mozman:mozman[2]'))
        # not only strings allowed
        self.assertTrue(self.checker.is_name(100))
        self.assertTrue(self.checker.is_name(100.123))

    def test_is_not_name(self):
        self.assertFalse(self.checker.is_name('mozman,mozman[2]'))
        self.assertFalse(self.checker.is_name('mozman mozman[2]'))
        self.assertFalse(self.checker.is_name('mozman(mozman)[2]'))
        # tuple and dict contains ',', '(', ')' or ' '
        self.assertFalse(self.checker.is_name((100, 200)))
        self.assertFalse(self.checker.is_name(dict(a=100, b=200)))

    def test_is_length(self):
        for value in [' 100px ', ' -100ex ', ' 100em ', ' -100pt ',
                      ' 100pc ', ' 100mm', ' 100cm', ' 100in',
                      ' 5%', 100, 3.1415, 700000, -500000, '100000',
                      '-4000000.45']:
            self.assertTrue(self.checker.is_length(value))
    def test_is_not_length(self):
        for value in [' 100xpx ', ' -100km ', ' 100mi ', (1, 1),
                      dict(a=1, b=2), [1, 2], ' mozman ']:
            self.assertFalse(self.checker.is_length(value))

    def test_is_integer(self):
        """ Integer also as String '100'. """
        # big numbers only valid for full profile
        self.assertTrue(self.checker.is_number(100000))
        self.assertTrue(self.checker.is_number(-100000))
        self.assertTrue(self.checker.is_number('100000'))
        self.assertTrue(self.checker.is_number('-100000'))
    def test_is_not_integer(self):
        self.assertFalse(self.checker.is_number( (1,2) ))
        self.assertFalse(self.checker.is_number('manfred'))
        self.assertFalse(self.checker.is_number( dict(a=1, b=2) ))
        self.assertTrue(self.checker.is_number(3.141592))
        self.assertTrue(self.checker.is_number('3.141592'))

    def test_is_percentage(self):
        self.assertTrue(self.checker.is_percentage(100))
        self.assertTrue(self.checker.is_percentage(50.123))
        self.assertTrue(self.checker.is_percentage(1000))
        self.assertTrue(self.checker.is_percentage('100'))
        self.assertTrue(self.checker.is_percentage('50.123'))
        self.assertTrue(self.checker.is_percentage('1000'))
        self.assertTrue(self.checker.is_percentage(' 100% '))
        self.assertTrue(self.checker.is_percentage(' 50.123% '))
        self.assertTrue(self.checker.is_percentage(' 1000% '))
    def test_is_not_percentage(self):
        self.assertFalse(self.checker.is_percentage('100px'))
        self.assertFalse(self.checker.is_percentage('100cm'))
        self.assertFalse(self.checker.is_percentage(' mozman '))
        self.assertFalse(self.checker.is_percentage( (1, 2) ))
        self.assertFalse(self.checker.is_percentage( dict(a=1, b=2) ))

    def test_is_time(self):
        self.assertTrue(self.checker.is_time(100))
        self.assertTrue(self.checker.is_time(50.123))
        self.assertTrue(self.checker.is_time(1000))
        self.assertTrue(self.checker.is_time(' 100 '))
        self.assertTrue(self.checker.is_time(' 50.123 '))
        self.assertTrue(self.checker.is_time(' 1000 '))
        self.assertTrue(self.checker.is_time(' 100ms'))
        self.assertTrue(self.checker.is_time(' 50.123s'))
        self.assertTrue(self.checker.is_time(' 1000ms'))
    def test_is_not_time(self):
        self.assertFalse(self.checker.is_time('100px'))
        self.assertFalse(self.checker.is_time('100cm'))
        self.assertFalse(self.checker.is_time(' mozman '))
        self.assertFalse(self.checker.is_time( (1, 2) ))
        self.assertFalse(self.checker.is_time( dict(a=1, b=2) ))

    def test_is_angle(self):
        self.assertTrue(self.checker.is_angle(100))
        self.assertTrue(self.checker.is_angle(50.123))
        self.assertTrue(self.checker.is_angle(1000))
        self.assertTrue(self.checker.is_angle(' 100 '))
        self.assertTrue(self.checker.is_angle(' 50.123 '))
        self.assertTrue(self.checker.is_angle(' 1000 '))
        self.assertTrue(self.checker.is_angle(' 100rad'))
        self.assertTrue(self.checker.is_angle(' 50.123grad'))
        self.assertTrue(self.checker.is_angle(' 1000deg'))
    def test_is_not_angle(self):
        self.assertFalse(self.checker.is_angle('100px'))
        self.assertFalse(self.checker.is_angle('100cm'))
        self.assertFalse(self.checker.is_angle(' mozman '))
        self.assertFalse(self.checker.is_angle( (1, 2) ))
        self.assertFalse(self.checker.is_angle( dict(a=1, b=2) ))

    def test_is_frequency(self):
        self.assertTrue(self.checker.is_frequency(100))
        self.assertTrue(self.checker.is_frequency(50.123))
        self.assertTrue(self.checker.is_frequency(1000))
        self.assertTrue(self.checker.is_frequency(' 100 '))
        self.assertTrue(self.checker.is_frequency(' 50.123 '))
        self.assertTrue(self.checker.is_frequency(' 1000 '))
        self.assertTrue(self.checker.is_frequency(' 100Hz'))
        self.assertTrue(self.checker.is_frequency(' 50.123kHz'))
        self.assertTrue(self.checker.is_frequency(' 1000Hz'))
    def test_is_not_frequency(self):
        self.assertFalse(self.checker.is_frequency('100px'))
        self.assertFalse(self.checker.is_frequency('100cm'))
        self.assertFalse(self.checker.is_frequency(' mozman '))
        self.assertFalse(self.checker.is_frequency( (1, 2) ))
        self.assertFalse(self.checker.is_frequency( dict(a=1, b=2) ))

    def test_is_shape(self):
        self.assertTrue(self.checker.is_shape(' rect(1, 2, 3, 4)'))
        self.assertTrue(self.checker.is_shape(' rect(1cm, 2mm, -3px, 4%)'))
    def test_is_not_shape(self):
        self.assertFalse(self.checker.is_shape('rect(1, 2, 3)'))
        self.assertFalse(self.checker.is_shape('rect(1, 2, 3, 4, 5)'))
        self.assertFalse(self.checker.is_shape('rect(1, 2, 3, m)'))

    def test_is_number_optional_number(self):
        self.assertTrue(self.checker.is_number_optional_number(' 1, 2'))
        self.assertTrue(self.checker.is_number_optional_number('1 2. '))
        self.assertTrue(self.checker.is_number_optional_number('1  '))
        self.assertTrue(self.checker.is_number_optional_number(' 1.5  '))
        self.assertTrue(self.checker.is_number_optional_number( 1 ))
        self.assertTrue(self.checker.is_number_optional_number( [1, 2] ))
    def test_is_not_number_optional_number(self):
        self.assertFalse(self.checker.is_number_optional_number(' 1px, 2'))
        self.assertFalse(self.checker.is_number_optional_number(' , 2'))
        self.assertFalse(self.checker.is_number_optional_number(' 1 , 2 , 3'))
        self.assertFalse(self.checker.is_number_optional_number(' 1. 2. 3.'))
        self.assertFalse(self.checker.is_number_optional_number(' 1 2 3'))
        self.assertFalse(self.checker.is_number_optional_number([]))
        self.assertFalse(self.checker.is_number_optional_number([1,2,3]))
        self.assertFalse(self.checker.is_number_optional_number([1, '1px']))
    def test_is_FuncIRI(self):
        self.assertTrue(self.checker.is_FuncIRI("url()"))
        self.assertTrue(self.checker.is_FuncIRI("url(http://localhost:8080?a=12)"))
        self.assertTrue(self.checker.is_FuncIRI("url(ftp://something/234)"))
    def test_is_not_FuncIRI(self):
        self.assertFalse(self.checker.is_FuncIRI("url"))
        self.assertFalse(self.checker.is_FuncIRI("url("))
        self.assertFalse(self.checker.is_FuncIRI("url(http://localhost:8080"))
        self.assertFalse(self.checker.is_FuncIRI("http://localhost:8080"))

if __name__=='__main__':
    unittest.main()