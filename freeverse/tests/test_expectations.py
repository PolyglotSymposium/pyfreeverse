#!/usr/bin/python3

import unittest

from freeverse import ActualValue, Should, Expect, It

class ShouldStyleAssertionsTests(unittest.TestCase):
    def test_basic_Actual_Value_should_method_takes_predicate(self):
        self.assertEqual('', ActualValue(4).should(lambda x: x == 4))
        self.assertEqual('Predicate not true of 4', ActualValue(4).should(lambda x: x == 2))

class ExpectStyleAssertionsTests(unittest.TestCase):
    def test_basic_Expect_to_method_takes_predicate(self):
        self.assertEqual('', Expect(4).to(lambda x: x == 4))
        self.assertGreater(len(Expect(4).to(lambda x: x == 2)), 0)

class ItStyleAssertionsTests(unittest.TestCase):
    def test_basic_It_should_method_takes_predicate(self):
        self.assertEqual('', It.should(lambda x: x == 4)(ActualValue(4)))
        self.assertGreater(len(It.should(lambda x: x == 2)(ActualValue(4))), 0)

if __name__ == '__main__':
    unittest.main()
