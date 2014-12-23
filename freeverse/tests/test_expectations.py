#!/usr/bin/python3

import unittest

from freeverse import ActualValue, Should, Expect, It

class ShouldStyleAssertionsTests(unittest.TestCase):
    def test_basic_actual_value_should_method_takes_predicate(self):
        self.assertEqual('', ActualValue(4).should(lambda x: x == 4))
        self.assertEqual('Predicate not true of 4', ActualValue(4).should(lambda x: x == 2))

    def test_actual_value_should_be_method_asserts_equality(self):
        self.assertEqual('', ActualValue(4).should_be(4))
        self.assertEqual('4 does not equal 2', ActualValue(4).should_be(2))

class ExpectStyleAssertionsTests(unittest.TestCase):
    def test_basic_expect_to_method_takes_predicate(self):
        self.assertEqual('', Expect(4).to(lambda x: x == 4))
        self.assertGreater(len(Expect(4).to(lambda x: x == 2)), 0)

    def test_expect_to_be_method_asserts_equality(self):
        self.assertEqual('', Expect(4).to_be(4))
        self.assertGreater(len(Expect(4).to_be(2)), 0)

class ItStyleAssertionsTests(unittest.TestCase):
    def test_basic_it_should_method_takes_predicate(self):
        self.assertEqual('', It.should(lambda x: x == 4)(ActualValue(4)))
        self.assertGreater(len(It.should(lambda x: x == 2)(ActualValue(4))), 0)

    def test_it_should_be_method_asserts_equality(self):
        self.assertEqual('', It.should_be(4)(ActualValue(4)))
        self.assertGreater(len(It.should_be(2)(ActualValue(4))), 0)

if __name__ == '__main__':
    unittest.main()
