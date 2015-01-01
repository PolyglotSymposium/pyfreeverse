#!/usr/bin/python3

import unittest

from freeverse import SpecFor, Should, Expect, It, FlatOutput
from freeverse.freeverse import TestStep, TestCase

class TestStepTests(unittest.TestCase):
    def test_runs_zero_argument_test_step(self):
        stepResult = TestStep('True', lambda: True).run()
        self.assertTrue(stepResult)

    def test_passes_previous_step_result_to_one_argument_test_step(self):
        stepResult = TestStep('description', lambda x: x).run(7)
        self.assertEqual(7, stepResult)

    def test_partially_applies_previous_step_result_to_two_argument_test_step(self):
        stepResult = TestStep('Power function', lambda x, y: pow(x, y)).run(2)
        self.assertEqual(8, stepResult(3))

    def test_partially_applies_previous_step_result_to_two_argument_test_step(self):
        stepResult = TestStep('Power function', lambda x, y, z: x + y + z).run(1)
        self.assertEqual(6, stepResult(2, 3))

    @unittest.skip('This is a known issue')
    def test_does_not_blow_up_when_trying_to_introspect_on_builtin_function(self):
        stepResult = TestStep('Power function', pow).run(2)
        self.assertEqual(8, stepResult(3))

class TestCaseTests(unittest.TestCase):
    def test_runs_set_of_one_test(self):
        testResult = TestCase([TestStep('True', lambda: True)]).run()
        self.assertTrue(testResult)

    def test_passes_result_of_one_step_into_the_next(self):
        testResult = TestCase([
            TestStep('1024', lambda: 1024),
            TestStep('plus 313', lambda x: x + 313)
        ]).run()
        self.assertEqual(1337, testResult)

class FreeverseTests(unittest.TestCase):
    def setUp(self):
        self.spec = SpecFor('Tests for the Freeverse spec library')

    def test_simplest_passing_case(self):
        self.spec.add('True', lambda: True, Should('be true', lambda t: t.should_equal(True)))

        result = self.spec.run()

        self.assertEqual('Tests for the Freeverse spec library', result.description())
        result = result.children()[0]
        self.assertEqual('True', result.description())
        self.assertTrue(result.passed())
        first_child = result.children()[0]
        self.assertEqual('should be true', first_child.description())
        self.assertTrue(first_child.passed())
        self.assertEqual('', first_child.message())

    def test_simplest_failing_case(self):
        self.spec.add('Two', lambda: 2, Should('be false', lambda t: t.should_equal(False)))

        result = self.spec.run().children()[0]

        self.assertEqual('Two', result.description())
        self.assertTrue(result.passed())
        first_child = result.children()[0]
        self.assertEqual('should be false', first_child.description())
        self.assertFalse(first_child.passed())
        self.assertEqual('2 does not equal False', first_child.message())

    def test_if_parent_fails_children_are_not_run(self):
        self.spec.add('The first element of an empty list', lambda: [][1], Should('boom!', lambda t: None))

        result = self.spec.run().children()[0]

        self.assertFalse(result.passed())
        self.assertEqual('IndexError raised: list index out of range', result.message())
        self.assertEqual(0, len(result.children()))

    def test_should_phrase_formats_error_messages(self):
        self.spec.add('This test', lambda: None, Should('fail because of an exception', lambda x: [][1]))

        result = self.spec.run().children()[0]

        result = result.children()[0]
        self.assertFalse(result.passed())
        self.assertEqual('IndexError raised: list index out of range', result.message())

    def test_supports_expect_phrases(self):
        self.spec.add('No matter what', lambda: None, ('1 equals 1', lambda: Expect(1).to_equal(1)))

        result = self.spec.run().children()[0]

        first_child = result.children()[0]
        self.assertEqual('1 equals 1', first_child.description())
        self.assertTrue(first_child.passed())

    def test_expect_phrase_formats_error_messages(self):
        self.spec.add('This test', lambda: [], ('fails because of an exception', lambda x: x[1]))

        result = self.spec.run().children()[0]

        result = result.children()[0]
        self.assertFalse(result.passed())
        self.assertEqual('IndexError raised: list index out of range', result.message())

    def test_it_style_shorthand(self):
        self.spec.add('True', True, Should('be true', It.should_equal(True)))

        result = self.spec.run()

        result = result.children()[0]
        self.assertTrue(result.passed())
        first_child = result.children()[0]
        self.assertEqual('', first_child.message())
        self.assertTrue(first_child.passed())

import io

class FlatOutputterTests(unittest.TestCase):
    def setUp(self):
        self.spec = SpecFor('Tests for the Freeverse spec library')

    def test_simple_passing_case(self):
        self.spec.add('True', True, Should('be true', It.should_equal(True)))

        with io.StringIO() as stream:
            outputter = FlatOutput(stream)
            self.spec.run_and_write_to(outputter)
            output = stream.getvalue()

        expected = ('Tests for the Freeverse spec library\n'
                    '\tTrue should be true\n')
        self.assertEqual(expected, output)

    @unittest.skip("Need to get this whole project factored better first")
    def test_complex_case(self):
        self.spec.add('The square', lambda: lambda x: x**2,
            ('of 0', lambda square: square(0),
                Should('be 0', It.should_be(0)),
                Should('be an idempotent operation', It.should_be(0))),
            ('of 1', lambda square: square(1),
                Should('be 1', It.should_be(1)),
                Should('be an idempotent operation', It.should_be(1))),
            ('of 2', lambda square: square(2),
                Should('be 4', It.should_be(4)),
                Should('not be an idempotent operation', It.should_not_be(1))),
        )

        with io.StringIO() as stream:
            outputter = FlatOutput(stream)
            self.spec.run_and_write_to(outputter)
            output = stream.getvalue()

        expected = ('Tests for the Freeverse spec library\n'
                    '\tThe square of 0 should be 0\n'
                    '\tThe square of 0 should be an idempotent operation\n'
                    '\tThe square of 1 should be 1\n'
                    '\tThe square of 1 should be an idempotent operation\n'
                    '\tThe square of 2 should be 4\n'
                    '\tThe square of 2 should not be an idempotent operation\n')
        print(expected)
        print(output)
        self.assertEqual(expected, output)

if __name__ == '__main__':
    #unittest.main()
    spec = SpecFor('Tests for the Freeverse spec library')
    spec.add('The square', lambda: lambda x: x**2,
        ('of 0', lambda square: square(0),
            Should('be 0', It.should_be(0)),
            Should('be an idempotent operation', It.should_be(0))),
        ('of 1', lambda square: square(1),
            Should('be 1', It.should_be(1)),
            Should('be an idempotent operation', It.should_be(1))),
        ('of 2', lambda square: square(2),
            Should('be 4', It.should_be(4)),
            Should('not be an idempotent operation', It.should_not_be(1))),
    )

    with io.StringIO() as stream:
        outputter = FlatOutput(stream)
        spec.run_and_write_to(outputter)
        output = stream.getvalue()

    expected = ('Tests for the Freeverse spec library\n'
                '\tThe square of 0 should be 0\n'
                '\tThe square of 0 should be an idempotent operation\n'
                '\tThe square of 1 should be 1\n'
                '\tThe square of 1 should be an idempotent operation\n'
                '\tThe square of 2 should be 4\n'
                '\tThe square of 2 should not be an idempotent operation\n')
    print(expected)
    print(output)
