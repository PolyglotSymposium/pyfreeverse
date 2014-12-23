# Freeverse for Python
## Free-form, minimalistic specs (tests) that favor natural language

I'm trying to pioneer a new style of specs. So far I have just slapped a bunch
of code together as a sort of brain dump. Soon it will be time to slow down and
begin to shape this code more carefully.

The basic idea is that you should be able to shape the spec how you want to
around the shape of your code and of the natural language descriptions you want
to use.

Freeverse supports a hierarchical/nested spec of this form:

    (<description>, <code-clause>, (<sub-specs>))

or for the leaf nodes:

    Verify(<description>, <code-clause>)

or

    Should(<description>, <code-clause>)

For example:

```python
from freeverse import SpecFor, Should, Expect, It
spec = SpecFor('README examples')

spec.add('5', lambda: 5,
    ('plus', lambda x: lambda y: x + y,
        ('2', lambda plus5: plus5(2), Should('be 7', It.should_be(7))),
        ('5', lambda plus5: plus5(5), Should('be 9', lambda nine: nine.should_be(9)))
    )
)

spec.add('An empty list', lambda: [], ('has a len() of zero', lambda l: Expect(len(l)).to_equal(0)))
```

The top-level tuple is passed into the `spec` function which parses and
registers the spec. The idea is to have largely free-forms specs that emphasize
human readability and structuring the specs in a way that makes sense for the
particular application. They are particularly designed for
input-transform-output type code (i.e. functional) though they could work in
other cases too, conceivably. The code-clauses are chained, i.e. the output of
one is piped into the next. The `should` function wraps the argument to its
code-clause in an object which allows should-style assertions on it. Also it
appends the word "should" to the beginning of that description of that clause
The alternative is to use the `expect` function for expect-style assertions in a
leaf node that has not been wrapped with should. This should also reduce code
duplication because you can easy form a set of tests around one object or action
and do not have to repeat those since you can break the code down into
"clauses". Also, there is a Result object which is illustrated below. In case it
was not clear above, the piping would be independent for each leaf node; i.e.
take the second spec (the one for 5) above. It will execute like this, where '|'
represents the result of one thing being piped in to the next:

    5 | +2 | 7 | passed
    5 | +5 | 10 | failed

And these two execution sequences are independent and could be run in
parallel. The output will look like this:

    5 plus 2 should be 7
    5 plus 5 should be 9

or the like, depending on ouputter.
