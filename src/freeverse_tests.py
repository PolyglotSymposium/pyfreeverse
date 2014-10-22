#!/usr/bin/python3

import unittest

from freeverse import SpecsFor, should

specs = SpecsFor('Tests for the Freeverse spec library')

class FreeverseTests(unittest.TestCase):
    def test_simplest_passing_case(self):
        specs.add('True', lambda: True, should('be true', lambda t: t.should_be(True)))

        result = specs.run()

        self.assertEqual('True', result.description())
        self.assertTrue(result.passed())
        self.assertEqual('be true', result.children()[0].description())
        self.assertTrue(result.children()[0].passed())

if __name__ == '__main__':
    unittest.main()
