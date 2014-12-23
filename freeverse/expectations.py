class ActualValue:
    def __init__(self, actual_value):
        self.__actual_value = actual_value

    def should(self, predicate):
        if predicate(self.__actual_value):
            return ''
        else:
            return 'Predicate not true of %s' % self.__actual_value

    def should_equal(self, expected_value):
        if self.__actual_value == expected_value:
            return ''
        else:
            return '%s does not equal %s' % (self.__actual_value, expected_value)
    should_be = should_equal

    def should_not_equal(self, expected_value):
        if self.__actual_value != expected_value:
            return ''
        else:
            return '%s does equal %s' % (self.__actual_value, expected_value)
    should_not_be = should_not_equal

class Expect:
    def __init__(self, actual_value):
        self.__actual_value = ActualValue(actual_value)

    def __getattr__(self, name):
        if name.startswith('to'):
            return getattr(self.__actual_value, 'should' + name[2:])
        else:
            raise AttributeError

It = lambda: It
for method_name in dir(ActualValue):
    if method_name.startswith('should'):
        (lambda method_name:
            setattr(It, method_name,
                lambda expected:
                    lambda actual_value: getattr(actual_value, method_name)(expected))
        )(method_name)

