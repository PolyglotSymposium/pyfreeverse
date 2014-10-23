#!/usr/bin/python3

import unittest

from freeverse import SpecsFor, should

class FreeverseTests(unittest.TestCase):
    def test_simplest_passing_case(self):
        specs = SpecsFor('Tests for the Freeverse spec library')
        specs.add('True', lambda: True, should('be true', lambda t: t.should_equal(True)))

        result = specs.run()

        self.assertEqual('Tests for the Freeverse spec library', result.description())
        result = result.children()[0]
        self.assertEqual('True', result.description())
        self.assertTrue(result.passed())
        first_child = result.children()[0]
        self.assertEqual('be true', first_child.description())
        self.assertTrue(first_child.passed())
        self.assertEqual('', first_child.message())

    def test_simplest_failing_case(self):
        specs = SpecsFor('Tests for the Freeverse spec library')
        specs.add('Two', lambda: 2, should('be false', lambda t: t.should_equal(False)))

        result = specs.run().children()[0]

        self.assertEqual('Two', result.description())
        self.assertTrue(result.passed())
        first_child = result.children()[0]
        self.assertEqual('be false', first_child.description())
        self.assertFalse(first_child.passed())
        self.assertEqual('2 does not equal False', first_child.message())

if __name__ == '__main__':
    unittest.main()
