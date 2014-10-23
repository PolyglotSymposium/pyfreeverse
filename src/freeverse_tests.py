#!/usr/bin/python3

import unittest

from freeverse import SpecsFor, Should, Expect

class FreeverseTests(unittest.TestCase):
    def test_simplest_passing_case(self):
        specs = SpecsFor('Tests for the Freeverse spec library')
        specs.add('True', lambda: True, Should('be true', lambda t: t.should_equal(True)))

        result = specs.run()

        self.assertEqual('Tests for the Freeverse spec library', result.description())
        result = result.children()[0]
        self.assertEqual('True', result.description())
        self.assertTrue(result.passed())
        first_child = result.children()[0]
        self.assertEqual('should be true', first_child.description())
        self.assertTrue(first_child.passed())
        self.assertEqual('', first_child.message())

    def test_simplest_failing_case(self):
        specs = SpecsFor('Tests for the Freeverse spec library')
        specs.add('Two', lambda: 2, Should('be false', lambda t: t.should_equal(False)))

        result = specs.run().children()[0]

        self.assertEqual('Two', result.description())
        self.assertTrue(result.passed())
        first_child = result.children()[0]
        self.assertEqual('should be false', first_child.description())
        self.assertFalse(first_child.passed())
        self.assertEqual('2 does not equal False', first_child.message())

    def test_if_parent_fails_children_are_not_run(self):
        specs = SpecsFor('Tests for the Freeverse spec library')
        specs.add('The first element of an empty list', lambda: [][1], Should('boom!', lambda t: None))

        result = specs.run().children()[0]

        self.assertFalse(result.passed())
        self.assertEqual('IndexError raised: list index out of range', result.message())
        self.assertEqual(0, len(result.children()))

    def test_should_phrase_formats_error_messages(self):
        specs = SpecsFor('Tests for the Freeverse spec library')
        specs.add('This test', lambda: None, Should('fail because of an exception', lambda x: [][1]))

        result = specs.run().children()[0]

        result = result.children()[0]
        self.assertFalse(result.passed())
        self.assertEqual('IndexError raised: list index out of range', result.message())

    def test_supports_expect_phrases(self):
        specs = SpecsFor('Tests for the Freeverse spec library')
        specs.add('No matter what', lambda: None, ('1 equals 1', lambda: Expect(1).to_equal(1)))

        result = specs.run().children()[0]

        first_child = result.children()[0]
        self.assertEqual('1 equals 1', first_child.description())
        self.assertTrue(first_child.passed())

    def test_expect_phrase_formats_error_messages(self):
        specs = SpecsFor('Tests for the Freeverse spec library')
        specs.add('This test', lambda: [], ('fails because of an exception', lambda x: x[1]))

        result = specs.run().children()[0]

        result = result.children()[0]
        self.assertFalse(result.passed())
        self.assertEqual('IndexError raised: list index out of range', result.message())

if __name__ == '__main__':
    unittest.main()
