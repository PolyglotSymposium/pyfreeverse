#!/usr/bin/python3

import unittest

from freeverse import Should, Expect, It
from freeverse.expectations import ActualValue

class ExpectationTests(unittest.TestCase):
    def assertIsNotEmpty(self, sizedObject):
        self.assertGreater(len(sizedObject), 0)

# Test the actual message here
class ShouldStyleAssertionsTests(ExpectationTests):
    def test_basic_actual_value_should_method_takes_predicate(self):
        self.assertEqual('', ActualValue(4).should(lambda x: x == 4))
        self.assertEqual('Predicate not true of 4', ActualValue(4).should(lambda x: x == 2))

    def test_actual_value_should_be_method_asserts_equality(self):
        self.assertEqual('', ActualValue(4).should_be(4))
        self.assertEqual('4 does not equal 2', ActualValue(4).should_be(2))

# The error message should be the same as the for the cases above, so only test
# that it is nonempty
class ExpectStyleAssertionsTests(ExpectationTests):
    def test_basic_expect_to_method_takes_predicate(self):
        self.assertEqual('', Expect(4).to(lambda x: x == 4))
        self.assertIsNotEmpty(Expect(4).to(lambda x: x == 2))

    def test_expect_to_be_method_asserts_equality(self):
        self.assertEqual('', Expect(4).to_be(4))
        self.assertIsNotEmpty(Expect(4).to_be(2))

# The error message should be the same as the for the cases above, so only test
# that it is nonempty
class ItStyleAssertionsTests(ExpectationTests):
    def test_basic_it_should_method_takes_predicate(self):
        self.assertEqual('', It.should(lambda x: x == 4)(ActualValue(4)))
        self.assertIsNotEmpty(It.should(lambda x: x == 2)(ActualValue(4)))

    def test_it_should_be_method_asserts_equality(self):
        self.assertEqual('', It.should_be(4)(ActualValue(4)))
        self.assertIsNotEmpty(It.should_be(2)(ActualValue(4)))

if __name__ == '__main__':
    unittest.main()
